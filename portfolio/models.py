from django.db import models
from accounts.models import Account

# Create your models here.
class Portfolio(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    dividends_target = models.FloatField(default=0.0, blank=False)

    def __str__(self) -> str:
        return self.user.email
    
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
    
class PortfolioItems(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10, blank=False)
    sort_of = models.CharField(max_length=15, choices=sort_of_choices, blank=False)
    quantity = models.IntegerField(blank=False)
    average_price = models.FloatField(blank=False)
    portfolio_weight = models.FloatField(default=0.0, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.portfolio} - {self.ticker} - {self.quantity}"
