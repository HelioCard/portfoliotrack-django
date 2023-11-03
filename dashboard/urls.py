from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('get_dashboard_data/', views.get_dashboard_data, name='get_dashboard_data'),
]