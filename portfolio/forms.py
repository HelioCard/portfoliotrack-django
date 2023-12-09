from django import forms
from .models import Portfolio

class UpdatePortfolioDividendsTarget(forms.ModelForm):
    dividends_target = forms.FloatField(
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Insira a nova Meta',
                'aria-label': 'target',
                'aria-describedby': "basic-addon1",
            }
        )
    )

    class Meta:
        model = Portfolio
        fields = ['dividends_target',]

    def clean(self):
        cleaned_data = super(UpdatePortfolioDividendsTarget, self).clean()
        dividends_target = cleaned_data.get('dividends_target')
        if dividends_target <= 0:
            raise forms.ValidationError('A meta deve ser maior que zero!')
