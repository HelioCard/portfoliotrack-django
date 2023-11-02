from celery.result import AsyncResult
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def check_process_raw_transactions_status(request, task_id):
    result = AsyncResult(task_id)

    if result.status == 'FAILURE':
        messages.error(request, f'Erro ao carregar as transações: {result.result}')
    elif result.status == 'SUCCESS':
        messages.success(request, 'Transações adicionadas com sucesso!')

    response_data = {'status': result.status}
    return JsonResponse(response_data)