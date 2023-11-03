from celery import shared_task
from django_celery_results.models import TaskResult
from django.utils import timezone
from helpers.TransactionsFromFile import TransactionsFromFile

@shared_task
def clean_expired_tasks():
    time_to_expire = timezone.now() - timezone.timedelta(minutes=60)
    print(time_to_expire)
    expired_tasks = TaskResult.objects.filter(date_done__lt=time_to_expire)
    count = expired_tasks.count()
    expired_tasks.delete()
    return f'SUCCESS: {count} tasks deleted!'

@shared_task
def process_raw_transactions(transactions_list):
    clean_expired_tasks.delay() # ==>TODO: Criar uma tarefa agendada para executar uma vez por hora.
    try:
        result = TransactionsFromFile().process_raw_transactions(transactions_list)
        if isinstance(result, tuple):
            print(result[2])
            # Processar os dados aqui...
            return 'SUCCESS'
        else:
            raise ValueError(result)
    except Exception as e:
        raise Exception(f'ERROR: {e}')


