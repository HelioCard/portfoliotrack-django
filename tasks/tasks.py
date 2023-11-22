from celery import shared_task
from django_celery_results.models import TaskResult
from django.utils import timezone
from helpers.TransactionsFromFile import TransactionsFromFile
from helpers.Cache.cache import session

from portfolio.models import Portfolio, Transactions
MINUTES_TO_EXPIRE = 30

@shared_task
def clean_expired_tasks():
    time_to_expire = timezone.datetime.now() - timezone.timedelta(minutes=MINUTES_TO_EXPIRE)
    expired_tasks = TaskResult.objects.filter(date_done__lt=time_to_expire)
    count = expired_tasks.count()
    expired_tasks.delete()
    session.cache.delete(expired=True)
    return f'SUCCESS: {count} tasks deleted!'

@shared_task
def register_transactions(raw_transactions_list, user_id):
    clean_expired_tasks.delay() # ==>TODO: Criar uma tarefa agendada para executar uma vez por hora.
    try:        
        transactions = process_transactions(transactions_list=raw_transactions_list, user_id=user_id)
        if isinstance(transactions, list):
            bulk_create_of_transactions(transactions=transactions, user_id=user_id)
            return 'SUCCESS'
        else:
            raise ValueError(transactions)
    except Exception as e:
        raise Exception(f'ERROR: {e}')

@shared_task
def update_transaction(edited_transaction, user_id, pk):
    try:       
        processed_transactions = process_transactions(transactions_list=edited_transaction, user_id=user_id)
        if isinstance(processed_transactions, list):
            # Se houver mais de um item na lista é porque há eventos de split/agrupamento a ser processado
            # devido a mudança de data na transação:
            if len(processed_transactions) > 1:
                events_to_add = []
                # Obtem os dados de eventos de split/agrupamentos e os envia para inclusão:
                for i, data in enumerate(processed_transactions):
                    if data['operation'] == 'A':
                        events_to_add.append(processed_transactions.pop(i))
                bulk_create_of_transactions(transactions=events_to_add, user_id=user_id)
            # Atualiza os dados da transação:
            transaction = Transactions.objects.get(id=pk)
            transaction.date = processed_transactions[0]['date']
            transaction.ticker = processed_transactions[0]['ticker']
            transaction.operation = processed_transactions[0]['operation']
            transaction.quantity = processed_transactions[0]['quantity']
            transaction.unit_price = processed_transactions[0]['unit_price']
            transaction.sort_of = processed_transactions[0]['sort_of']
            transaction.save()
            # Obtem a lista de ticker, para atualização dos eventos. Exemplo: se a data de uma transação for alterada e for necessária
            # a exclusão de um evento de split/agrupamento:
            list_of_ticker = [transaction.ticker]
            update_events_of_transactions(list_of_tickers=list_of_ticker, user_id=user_id)
            return 'SUCCESS'
        else:
            raise ValueError(processed_transactions)
    except Exception as e:
        raise Exception(f'ERROR: {e}')

@shared_task
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

@shared_task
def process_transactions(transactions_list, user_id):
    existing_events = Transactions.objects.filter(portfolio__user_id=user_id, operation="A")
    existing_events_list = list(existing_events.values())
    return TransactionsFromFile().process_raw_transactions(transactions_list, existing_events_list)

@shared_task
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
