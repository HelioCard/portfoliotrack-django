from django.contrib import admin
from .models import Portfolio, PortfolioItems

# Register your models here.
class PortfolioAdmin(admin.ModelAdmin):
    list_display = ['user', 'dividends_target']

class PortfolioItemsAdmin(admin.ModelAdmin):
    list_display = ['portfolio', 'ticker', 'sort_of', 'quantity', 'average_price', 'portfolio_weight', 'is_active', 'created_at', 'updated_at']

admin.site.register(Portfolio, PortfolioAdmin)
admin.site.register(PortfolioItems, PortfolioItemsAdmin)