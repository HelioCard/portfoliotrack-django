from collections.abc import Mapping
from typing import Any
from django import forms
from django.core.files.base import File
from django.db.models.base import Model
from django.forms.utils import ErrorList
from .models import Account
from django.utils.translation import gettext as _

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Senha',
        'class': 'form-control',
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repita a Senha',
        'class': 'form-control'
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password']

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
        self.fields['first_name'].widget.attrs['placeholder'] = 'Nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Sobrenome'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        email = cleaned_data.get('email')

        if password != confirm_password:
            raise forms.ValidationError(
                'As senhas inseridas não conferem!'
            )
        
        if Account.objects.filter(email=email).exists():
            raise forms.ValidationError(_(f'Uma conta com o email {email} já existe!'))

class EditUserForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nome',
        'id': 'floatingFirstName',
        'class': 'form-control',
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Sobrenome',
        'id': 'floatingLastName',
        'class': 'form-control',
    }))
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Nome de Usuário',
        'id': 'floatingUserName',
        'class': 'form-control',
    }))
    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'username']

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)
    