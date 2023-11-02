from django.shortcuts import render, redirect
from .forms import UploadFormFile
from django.contrib import messages
from tasks.tasks import process_raw_transactions
from helpers.TransactionsFromFile import TransactionsFromFile

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx'):
                
                transactions_list = TransactionsFromFile().load_file(file)
                task = process_raw_transactions.delay(transactions_list)
                
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

