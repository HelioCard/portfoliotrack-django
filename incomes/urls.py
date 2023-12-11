from django.urls import path
from . import views

urlpatterns = [
    path('history/', views.history, name='history'),
    path('get_incomes_history/', views.get_incomes_history, name='get_incomes_history'),
    path('evolution/', views.evolution, name='evolution'),
]