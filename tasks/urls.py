from django.urls import path, include
from . import views

urlpatterns = [
    path('check_process_raw_transactions_status/<task_id>/', views.check_process_raw_transactions_status, name='check_process_raw_transactions_status')
]