from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('balance/', views.balance, name='balance'),
    path('get_portfolio_summary/<str:subtract_dividends>/', views.get_portfolio_summary, name='get_portfolio_summary'),
    path('get_balance_data/', views.get_balance_data, name='get_balance_data'),
]