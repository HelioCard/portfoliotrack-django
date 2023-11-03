from celery import shared_task
from helpers.TransactionsFromFile import TransactionsFromFile

@shared_task
def process_raw_transactions(transactions_list):
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


