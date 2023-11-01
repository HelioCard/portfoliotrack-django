from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('get_portfolio_performance_chart/', views.get_portfolio_performance_chart, name='get_portfolio_performance_chart'),
    path('get_category_chart/', views.get_category_chart, name='get_category_chart'),
    path('get_asset_chart/', views.get_asset_chart, name='get_asset_chart'),
]