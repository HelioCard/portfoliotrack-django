from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('get_dashboard_data/<str:subtract_dividends>/', views.get_dashboard_data, name='get_dashboard_data'),
]