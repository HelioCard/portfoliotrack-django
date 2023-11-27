from django.db import models
from portfolio.models import Portfolio

# Create your models here.
sort_of_choices = [
        ('AÇÕES', 'AÇÕES'),
        ('FIIS', 'FIIS'),
        ('SPLIT/AGRUP', 'SPLIT/AGRUP'),
    ]

operation_choices = [
        ('C', 'COMPRA'),
        ('V', 'VENDA'),
        ('A', 'SPLIT/AGRUP'),
    ]

class Transactions(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    date = models.DateField()
    ticker = models.CharField(max_length=10, blank=False)
    operation = models.CharField(max_length=3, choices=operation_choices, blank=False)
    quantity = models.IntegerField(blank=False)
    unit_price = models.FloatField(blank=False)
    sort_of = models.CharField(max_length=15, choices=sort_of_choices, blank=False)
    
    def __str__(self) -> str:
        return f"{self.portfolio} - {self.operation} de {self.ticker} em {self.date} a {self.unit_price}"
    
    def get_operation_display_full(self):
        operation_dict = dict(operation_choices)
        return operation_dict.get(self.operation, self.operation)