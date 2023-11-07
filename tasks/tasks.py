from celery import shared_task
from django_celery_results.models import TaskResult
from django.utils import timezone
from helpers.TransactionsFromFile import TransactionsFromFile

from portfolio.models import Portfolio, Transactions

@shared_task
def clean_expired_tasks():
    time_to_expire = timezone.datetime.now() - timezone.timedelta(minutes=30)
    expired_tasks = TaskResult.objects.filter(date_done__lt=time_to_expire)
    count = expired_tasks.count()
    expired_tasks.delete()
    return f'SUCCESS: {count} tasks deleted!'

@shared_task
def process_raw_transactions(raw_transactions_list, user_id):
    clean_expired_tasks.delay() # ==>TODO: Criar uma tarefa agendada para executar uma vez por hora.
    try:
        existing_events = Transactions.objects.filter(portfolio__user_id=user_id, operation="A")
        existing_events_list = list(existing_events.values())
        
        result = TransactionsFromFile().process_raw_transactions(raw_transactions_list, existing_events_list)
        
        if isinstance(result, list):

            portfolio = Portfolio.objects.get(user_id=user_id)
            fulldataset = []
            for data in result:
                tempdata = Transactions(portfolio=portfolio, date=data['date'], ticker=data['ticker'], operation=data['operation'], quantity=data['quantity'], unit_price=data['unit_price'], sort_of=data['sort_of'])
                fulldataset.append(tempdata)

            Transactions.objects.bulk_create(fulldataset)

            return 'SUCCESS'
        else:
            raise ValueError(result)
    except Exception as e:
        raise Exception(f'ERROR: {e}')

