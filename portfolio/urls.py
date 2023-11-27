from django.urls import path
from . import views

urlpatterns = [
    path('summary/', views.summary, name='summary'),
    path('get_portfolio_summary/<str:subtract_dividends>/', views.get_portfolio_summary, name='get_portfolio_summary'),
]