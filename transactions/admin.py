from django.contrib import admin
from .models import Transactions

# Register your models here.
class TransactionsAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'date', 'ticker', 'operation', 'quantity', 'unit_price', 'sort_of']

admin.site.register(Transactions, TransactionsAdmin)