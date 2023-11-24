from django.shortcuts import render, redirect
from .forms import UploadFormFile, RegisterTransactionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse, JsonResponse
from django.conf import settings

from tasks.tasks import register_transactions, update_transaction, update_events_of_transactions
from helpers.TransactionsFromFile import TransactionsFromFile
from helpers.DashboardChartsProcessing import DashboardChartsProcessing
from .models import Transactions

import os
import datetime

# Create your views here.
@login_required(login_url='login')
def transactions(request):
    transactions = Transactions.objects.filter(portfolio__user=request.user).order_by('-date')
    context = {
        'transactions': transactions,
    }
    return render(request, 'transactions.html', context)

@login_required(login_url='login')
def download_model_file(request):
    file_path = os.path.join(settings.STATIC_ROOT, 'media/modelo.xlsx')
    return FileResponse(open(file_path, 'rb'), as_attachment=True)

@login_required(login_url='login')
def upload_file(request):
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']   
            user_id = request.user.id
            raw_transactions_list = TransactionsFromFile().load_file(file)
            task = register_transactions.delay(raw_transactions_list, user_id)
            messages.success(request, f'Processando transações do arquivo "{file}". Aguarde ...')
            context = {
                'task_id': task.task_id,
                'redirect_url': 'dashboard',
            }
            return render(request, 'processTransactions.html', context)
        else:
            messages.error(request, form.errors)        
    return redirect('dashboard')

@login_required(login_url='login')
def register_transaction(request):
    if request.method == 'POST':
        form = RegisterTransactionForm(request.POST)
        if form.is_valid():
            transaction = [
                {
                    'date': datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d'),
                    'ticker': request.POST['ticker'].upper(),
                    'operation': request.POST['operation'].upper(),
                    'quantity': int(request.POST['quantity']),
                    'unit_price': float(request.POST['unit_price']),
                    'sort_of': request.POST['sort_of'],
                }
            ]
            user_id = request.user.id             
            task = register_transactions.delay(transaction, user_id)
            messages.success(request, f"Processando transação de {transaction[0]['operation']} de {transaction[0]['ticker']}. Aguarde ...")
            context = {
                'task_id': task.task_id,
                'redirect_url': 'dashboard',
            }
            return render(request, 'processTransactions.html', context)
        else:
            messages.error(request, form.errors['__all__'])
    return redirect('dashboard')

@login_required(login_url='login')
def delete_transaction(request):
    if request.method == 'POST':
        user = request.user
        strings_of_ids = request.POST.get('ids')
        if not strings_of_ids:
            messages.error(request, 'Nenhuma transação selecionada!')
            return redirect('transactions')
        if strings_of_ids == 'all':
            transactions = Transactions.objects.filter(portfolio__user=user)
            transactions.delete()
            messages.success(request, 'Todas as suas transações foram apagadas com sucesso!')
            return redirect('transactions')
        try:
            list_of_ids = strings_of_ids.split(',')
            list_of_ids = [int(value) for value in list_of_ids]
            transactions = Transactions.objects.filter(pk__in=list_of_ids)
            list_of_tickers = TransactionsFromFile().extract_tickers_list(list(transactions.values())) # Obtem a lista de tickers das transações apagadas
            transactions.delete()
            update_events_of_transactions(list_of_tickers=list_of_tickers, user_id=user.id) # Atualiza os eventos de splits/agrupamentos
            messages.success(request, f'{len(list_of_ids)} transações apagadas com sucesso!')
            return redirect('transactions')
        except Exception as e:
            print(e)
            messages.error(request, f'Algo de errado: {str(e)}')
    return redirect('transactions')

@login_required(login_url='login')
def edit_transaction(request, pk):
    transaction = Transactions.objects.get(id=pk)
    if request.method == 'POST':
        form = RegisterTransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            edited_transaction = [
                {
                    'date': datetime.datetime.strptime(request.POST['date'], '%Y-%m-%d'),
                    'ticker': request.POST['ticker'].upper(),
                    'operation': request.POST['operation'].upper(),
                    'quantity': int(request.POST['quantity']),
                    'unit_price': float(request.POST['unit_price']),
                    'sort_of': request.POST['sort_of'],
                }
            ]
            user_id = request.user.id
            task = update_transaction.delay(edited_transaction, user_id, pk)
            messages.success(request, f"Processando alteração da transação: {edited_transaction[0]['operation']} de {edited_transaction[0]['ticker']}. Aguarde ...")

            context = {
                'task_id': task.task_id,
                'redirect_url': 'transactions',
            }
            return render(request, 'processTransactions.html', context)
    else:
        form = RegisterTransactionForm(instance=transaction)

    context = {
        'edit_transaction_form': form,
        'transaction_id': transaction.id,
    }
    return render(request, 'editTransaction.html', context)

@login_required(login_url='login')
def summary(request):
    return render(request, 'portfolioSummary.html')

@login_required(login_url='login')
def get_portfolio_summary(request):
    try:        
        processor = DashboardChartsProcessing(user=request.user, ticker=None, subtract_dividends_from_contribution='N')
        summary_data = processor.get_portfolio_summary()
        context = {
            'summary_data': summary_data,
        }
        return JsonResponse(context)
    except ValueError as e:
        return JsonResponse({'Erro': str(e)}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'Erro': str(e)}, status=500)