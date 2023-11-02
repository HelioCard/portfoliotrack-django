from celery import shared_task
from helpers.TransactionsFromFile import TransactionsFromFile

@shared_task
def process_trasactions(transactions_list):
    try:
        result = TransactionsFromFile().process_raw_trasactions(transactions_list)
        if isinstance(result, tuple):
            print(result[2])
            # Processar os dados aqui...
            return 'SUCCESS'
        else:
            raise ValueError(result)
    except Exception as e:
        return f'ERROR: {e}'


