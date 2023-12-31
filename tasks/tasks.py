from celery import shared_task
from django_celery_results.models import TaskResult
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from helpers.TransactionsFromFile import TransactionsFromFile
from helpers.Cache.cache import session

from portfolio.models import Portfolio, PortfolioItems
from transactions.models import Transactions
MINUTES_TO_EXPIRE = 30

@shared_task(expires=1800)
def clean_expired_tasks():
    time_to_expire = timezone.datetime.now() - timezone.timedelta(minutes=MINUTES_TO_EXPIRE)
    expired_tasks = TaskResult.objects.filter(date_done__lt=time_to_expire)
    count = expired_tasks.count()
    expired_tasks.delete()
    session.cache.delete(expired=True)
    return f'SUCCESS: {count} tasks deleted!'

@shared_task(expires=1800)
def register_transactions(raw_transactions_list, user_id):
    clean_expired_tasks.delay() # ==>TODO: Criar uma tarefa agendada para executar uma vez por hora.
    try:        
        transactions = process_transactions(transactions_list=raw_transactions_list, user_id=user_id)
        if isinstance(transactions, list):
            bulk_create_of_transactions(transactions=transactions, user_id=user_id)
            update_portfolio_items(user_id=user_id)
            return 'SUCCESS'
        else:
            raise ValueError(transactions)
    except Exception as e:
        raise Exception(f'ERROR: {e}')

@shared_task(expires=1800)
def update_transaction(edited_transaction, user_id, pk):
    try:
        # Valida os dados de entrada e insere eventos de split/agrup se houver:        
        processed_transactions = process_transactions(transactions_list=edited_transaction, user_id=user_id)
        if isinstance(processed_transactions, list):
            processed_transactions = register_split_group_events(processed_transactions=processed_transactions, user_id=user_id)
            
            # Atualiza os dados da transação:
            transaction = Transactions.objects.get(id=pk)

            # Obtem o ticker que foi editado antes que ele seja atualizado.
            # Em caso de troca de ticker e não haver outras transações do mesmo ticker, seus eventos de split/agrupamento precisam ser atualizados/excluídos:
            list_of_ticker = [transaction.ticker] 

            transaction.date = processed_transactions[0]['date']
            transaction.ticker = processed_transactions[0]['ticker']
            transaction.operation = processed_transactions[0]['operation']
            transaction.quantity = processed_transactions[0]['quantity']
            transaction.unit_price = processed_transactions[0]['unit_price']
            transaction.sort_of = processed_transactions[0]['sort_of']
            transaction.save()
            # Obtem a lista de ticker, para atualização dos eventos. Exemplo: se a data de uma transação for alterada e for necessária
            # a exclusão de um evento de split/agrupamento:
            print(list_of_ticker)
            update_events_of_transactions(list_of_tickers=list_of_ticker, user_id=user_id)
            update_portfolio_items(user_id=user_id)
            return 'SUCCESS'
        else:
            raise ValueError(processed_transactions)
    except Exception as e:
        raise Exception(f'ERROR: {e}')

@shared_task(expires=1800)
def update_events_of_transactions(list_of_tickers, user_id):
    # Percorre a lista de tickers verificando se há eventos de Split/Agrup salvos com datas anterior à operação mais velha do ticker
    # Se houver, apaga o evento. Se não houver mais operações do ticker, apaga todos os eventos
    for ticker in list_of_tickers:
        transactions_of_ticker = Transactions.objects.filter(portfolio__user_id=user_id, ticker=ticker, operation='C')
        events_of_ticker = Transactions.objects.filter(portfolio__user_id=user_id, ticker=ticker, operation='A')
        if not events_of_ticker:
            continue
        if not transactions_of_ticker:
            if events_of_ticker:
                events_of_ticker.delete()
            continue

        first_transaction = min(list(transactions_of_ticker.values()), key=lambda x: x['date'])
        
        for event in events_of_ticker:
            if event.date <= first_transaction['date']:
                event.delete()

@shared_task(expires=1800)
def process_transactions(transactions_list, user_id):
    existing_events = Transactions.objects.filter(portfolio__user_id=user_id, operation="A")
    existing_events_list = list(existing_events.values())
    return TransactionsFromFile().process_raw_transactions(transactions_list, existing_events_list)

@shared_task(expires=1800)
def bulk_create_of_transactions(transactions, user_id):
    portfolio = Portfolio.objects.get(user_id=user_id)
    fulldataset = []
    for data in transactions:
        tempdata = Transactions(
            portfolio=portfolio,
            date=data['date'],
            ticker=data['ticker'],
            operation=data['operation'],
            quantity=data['quantity'],
            unit_price=data['unit_price'],
            sort_of=data['sort_of']
        )
        fulldataset.append(tempdata)
    Transactions.objects.bulk_create(fulldataset)

@shared_task(expires=1800)
def register_split_group_events(processed_transactions, user_id):
    # Se houver mais de um item na lista é porque há eventos de split/agrupamento a ser processado
    # devido a mudança de data na transação:
    if len(processed_transactions) > 1:
        events_to_add = []
        edited_transaction = []
        # Separa os dados de eventos (split/agrupamentos) da transação editada pelo usuário.
        for data in processed_transactions:
            events_to_add.append(data) if data['operation'] == 'A' else edited_transaction.append(data)
        # Envia para inclusão os dados de eventos separados (se houver):
        if events_to_add:
            bulk_create_of_transactions(transactions=events_to_add, user_id=user_id)
        # Retorna somente a transação editada pelo usuário:
        return edited_transaction
    return processed_transactions

@shared_task(expires=1800)
def update_portfolio_items(user_id):
    # Busca as transações e calcula o balanço do portfolio:
    portfolio = Portfolio.objects.get(user_id=user_id)
    transactions = Transactions.objects.filter(portfolio__user_id=user_id).values()
    transactions_list = list(transactions)
    portfolio_items, _ = TransactionsFromFile().calculate_portfolio_balance_and_asset_history(transactions_list)
    # Busca os dados salvos no modelo PortfolioItems:
    saved_portfolio_items = PortfolioItems.objects.filter(portfolio__user_id=user_id)
    # Percorre os items do portfolio:
    for ticker, data in portfolio_items.items():
        try:
            obj = PortfolioItems.objects.get(portfolio=portfolio, ticker=ticker)
            # Quantidade >  0: Se o objeto já existir em PortfolioItems, ativa-o.
            if data['quantity'] > 0:
                obj.is_active = True
                obj.save()
            else: # Quantidade <= 0: Se o objeto existir, desativa-o:
                obj.is_active = False
                obj.save()
        except ObjectDoesNotExist:
            if data['quantity'] > 0:
                portfolio_item = PortfolioItems(portfolio=portfolio, ticker=ticker)
                portfolio_item.save()
            else:
                portfolio_item = PortfolioItems(portfolio=portfolio, ticker=ticker, is_active=False)
                portfolio_item.save()
    # Percorre os itens salvos no modelo PortfolioItems e verifica se há algum objeto salvo, mas que não consta das transações. Se encontrar, exclui:
    for item in saved_portfolio_items:
        if not portfolio_items.get(item.ticker):
            item.delete()

