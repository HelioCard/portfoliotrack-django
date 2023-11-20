from django.shortcuts import render, redirect
from .forms import UploadFormFile, RegisterTransactionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from tasks.tasks import process_raw_transactions
from helpers.TransactionsFromFile import TransactionsFromFile
from .models import Transactions

from django.http import FileResponse
from django.conf import settings
import os
import datetime

# Create your views here.
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
            if file.name.endswith('.xlsx'):
                
                user_id = request.user.id
                raw_transactions_list = TransactionsFromFile().load_file(file)

                task = process_raw_transactions.delay(raw_transactions_list, user_id)
                
                messages.success(request, f'Processando transações do arquivo "{file}". Aguarde ...')
                context = {
                    'task_id': task.task_id,
                }
                
                return render(request, 'upload_file.html', context)

            else:
                messages.error(request, f"Arquivo inválido: {file}. Baixe o modelo de arquivo apropriado no menu à esquerda, botão 'Carregar de Arquivo'.")
        else:
            messages.error(request, f"Arquivo inválido: {file}. Baixe o modelo de arquivo apropriado no menu à esquerda, botão 'Carregar de Arquivo'.")
            
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
                        
            task = process_raw_transactions.delay(transaction, user_id)
            
            messages.success(request, f"Processando transação de {transaction[0]['operation']} de {transaction[0]['ticker']}. Aguarde ...")
            context = {
                'task_id': task.task_id,
            }
            
            return render(request, 'upload_file.html', context)
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

            ##################################################################################################################################
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
            ##################################################################################################################################
                
            messages.success(request, f'{len(list_of_ids)} transações apagadas com sucesso!')
            return redirect('transactions')
        except Exception as e:
            print(e)
            messages.error(request, f'Algo de errado: {str(e)}')
        
    return redirect('transactions')

@login_required(login_url='login')
def transactions(request):
    transactions = Transactions.objects.filter(portfolio__user=request.user).order_by('-date')
    context = {
        'transactions': transactions,
    }
    return render(request, 'transactions.html', context)
