from celery import shared_task
from django_celery_results.models import TaskResult
from django.utils import timezone
from helpers.TransactionsFromFile import TransactionsFromFile
from helpers.Cache.cache import session

from portfolio.models import Portfolio, Transactions

@shared_task
def clean_expired_tasks():
    time_to_expire = timezone.datetime.now() - timezone.timedelta(minutes=30)
    expired_tasks = TaskResult.objects.filter(date_done__lt=time_to_expire)
    count = expired_tasks.count()
    expired_tasks.delete()
    session.cache.delete(expired=True)
    return f'SUCCESS: {count} tasks deleted!'

@shared_task
def process_raw_transactions(raw_transactions_list, user_id):
    clean_expired_tasks.delay() # ==>TODO: Criar uma tarefa agendada para executar uma vez por hora.
    try:
        existing_events = Transactions.objects.filter(portfolio__user_id=user_id, operation="A")
        existing_events_list = list(existing_events.values())
        
        transactions = TransactionsFromFile().process_raw_transactions(raw_transactions_list, existing_events_list)
        
        if isinstance(transactions, list):

            portfolio = Portfolio.objects.get(user_id=user_id)
            fulldataset = []
            for data in transactions:
                tempdata = Transactions(portfolio=portfolio, date=data['date'], ticker=data['ticker'], operation=data['operation'], quantity=data['quantity'], unit_price=data['unit_price'], sort_of=data['sort_of'])
                fulldataset.append(tempdata)

            Transactions.objects.bulk_create(fulldataset)

            return 'SUCCESS'
        else:
            raise ValueError(transactions)
    except Exception as e:
        raise Exception(f'ERROR: {e}')

@shared_task
def update_events_of_transactions(list_of_tickers, user):
    # Percorre a lista de tickers verificando se há eventos de Split/Agrup salvos com datas anterior à operação mais velha do ticker
    # Se houver, apaga o evento. Se não houver mais operações do ticker, apaga todos os eventos
    for ticker in list_of_tickers:
        transactions_of_ticker = Transactions.objects.filter(portfolio__user=user, ticker=ticker, operation='C')
        events_of_ticker = Transactions.objects.filter(portfolio__user=user, ticker=ticker, operation='A')
        if not events_of_ticker:
            continue
        if not transactions_of_ticker:
            if events_of_ticker:
                events_of_ticker.delete()
            continue

        first_transaction = min(list(transactions_of_ticker.values()), key=lambda x: x['date'])
        for event in events_of_ticker:
            if event.date <= first_transaction['date']:
                print(event)
                event.delete()