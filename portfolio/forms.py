from django import forms
from portfolio.models import Transactions
from datetime import date as dt
from datetime import datetime
import yfinance as yt
from helpers.Cache.cache import session

class UploadFormFile(forms.Form):
    file = forms.FileField(
        widget=forms.FileInput(
            attrs={
                'accept': '.xls, .xlsx',
                'class': 'form-control',
            }
        ),
        label='Selecione um arquivo Excel',
    )

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if uploaded_file:
            if not uploaded_file.name.endswith(('.xls', '.xlsx')):
                raise forms.ValidationError(f'Arquivo inválido: {uploaded_file}! Baixe o modelo correto no menu à esquerda, botão "Carregar de Arquivo"')
        return uploaded_file


class RegisterTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.TextInput(attrs={
        'placeholder': 'Data',
        'class': 'form-control',
        'type': 'text',
        'id': 'id_date',
        'autocomplete': 'off',
    }))

    class Meta:
        model = Transactions
        fields = ['date', 'ticker', 'operation', 'quantity', 'unit_price', 'sort_of']

    def __init__(self, *args, **kwargs):
        super(RegisterTransactionForm, self).__init__(*args, **kwargs)
        
        self.fields['ticker'].widget.attrs['placeholder'] = 'Ticker do Ativo'
        self.fields['operation'].widget.attrs['placeholder'] = 'Operação (C ou V)'
        self.fields['quantity'].widget.attrs['placeholder'] = 'Quantidade'
        self.fields['unit_price'].widget.attrs['placeholder'] = 'Preço Unitário'
        self.fields['sort_of'].widget.attrs['placeholder'] = 'Tipo (Ações ou FIIs)'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegisterTransactionForm, self).clean()
        date = cleaned_data.get('date')
        operation = cleaned_data.get('operation')
        quantity =  cleaned_data.get('quantity')
        if operation == 'A' and quantity != 0:
            raise forms.ValidationError('Para operações de split/agrupamento use quantidade = 0')
        if date > dt.today():
            raise forms.ValidationError('A data da operação é inválida!')
        
        
        

        
            