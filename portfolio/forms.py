from django import forms
from portfolio.models import Transactions
from datetime import date as dt
import yfinance as yt
from helpers.Cache.cache import session

class UploadFormFile(forms.Form):
    file = forms.FileField()


class RegisterTransactionForm(forms.ModelForm):
    date = forms.DateField(widget=forms.DateInput(attrs={
        'placeholder': 'Data',
        'class': 'form-control',
        'type': 'date',
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
        if date > dt.today():
            raise forms.ValidationError('A data da operação é inválida!')

        
            