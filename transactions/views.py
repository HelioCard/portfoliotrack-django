from django.shortcuts import render, redirect
from .forms import UploadFormFile, RegisterTransactionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist

from tasks.tasks import register_transactions, update_transaction, update_events_of_transactions, update_portfolio_items
from helpers.TransactionsFromFile import TransactionsFromFile
from .models import Transactions

import os
import datetime

# Create your views here.
@login_required(login_url='login')
def transactions(request):
    transactions = Transactions.objects.filter(portfolio__user=request.user).order_by('-date')
    url = request.path
    context = {
        'transactions': transactions,
        'url': url,
    }
    return render(request, 'transactions/transactions.html', context)

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
            try:
                raw_transactions_list = TransactionsFromFile().load_file(file)
                task = register_transactions.delay(raw_transactions_list, user_id)
                messages.success(request, f'Processando transações do arquivo "{file}". Enquanto processamos as transações você pode continuar navegando no site!')
                context = {
                    'task_id': task.task_id,
                    'redirect_url': 'dashboard',
                }
                return render(request, 'transactions/processTransactions.html', context)
            except Exception as e:
                messages.error(request, f'Erro: {e}')
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
            return render(request, 'transactions/processTransactions.html', context)
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
            update_portfolio_items(user_id=user.id)
            messages.success(request, 'Todas as suas transações foram apagadas com sucesso!')
            return redirect('transactions')
        try:
            list_of_ids = strings_of_ids.split(',')
            list_of_ids = [int(value) for value in list_of_ids]
            transactions = Transactions.objects.filter(pk__in=list_of_ids)
            list_of_tickers = TransactionsFromFile().extract_tickers_list(list(transactions.values())) # Obtem a lista de tickers das transações apagadas
            transactions.delete()
            update_events_of_transactions(list_of_tickers=list_of_tickers, user_id=user.id) # Atualiza os eventos de splits/agrupamentos
            update_portfolio_items(user_id=user.id)
            messages.success(request, f'{len(list_of_ids)} transações apagadas com sucesso!')
            return redirect('transactions')
        except Exception as e:
            print(e)
            messages.error(request, f'Algo deu errado: {str(e)}')
    return redirect('transactions')

@login_required(login_url='login')
def edit_transaction(request, pk):
    try:
        transaction = Transactions.objects.get(id=pk, portfolio__user=request.user)
    except ObjectDoesNotExist:
        messages.error(request, 'Transação inexistente!')
        return redirect('transactions')
    
    url = '/transactions/edit_transaction/'
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
            return render(request, 'transactions/processTransactions.html', context)
    else:
        form = RegisterTransactionForm(instance=transaction)
        context = {
            'edit_transaction_form': form,
            'transaction_id': transaction.id,
            'url': url,
        }
        return render(request, 'transactions/editTransaction.html', context)