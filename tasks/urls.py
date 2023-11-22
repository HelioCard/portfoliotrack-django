from django.urls import path, include
from . import views

urlpatterns = [
    path('check_tasks_status/<task_id>/', views.check_tasks_status, name='check_tasks_status')
]