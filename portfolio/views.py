from django.shortcuts import render, redirect
from .forms import UploadFormFile
from django.contrib import messages
from helpers.TransactionsFromFile import TransactionsFromFile

# Create your views here.
def upload_file(request):
    if request.method == 'POST':
        form = UploadFormFile(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            if file.name.endswith('.xlsx'):
                messages.success(request, f'Processando arquivo: {file}. Aguarde...')
                
                transactions = TransactionsFromFile().load_transactions_from_excel(file)
                print(transactions)
            else:
                messages.error(request, f"Arquivo inválido: {file}. Baixe o modelo de arquivo apropriado no menu à esquerda, botão 'Carregar de Arquivo'.")


    return redirect('dashboard')