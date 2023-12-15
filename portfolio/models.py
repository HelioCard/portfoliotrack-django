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

class PortfolioItems(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    ticker = models.CharField(max_length=10, blank=False)
    portfolio_weight = models.FloatField(default=50.0, blank=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.portfolio} - {self.ticker}"
