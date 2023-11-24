from django.urls import path
from . import views

urlpatterns = [
    path('upload_file/', views.upload_file, name="upload_file"),
    path('download_model_file/', views.download_model_file, name="download_model_file"),
    path('register_transaction/', views.register_transaction, name="register_transaction"),
    path('transactions/', views.transactions, name='transactions'),
    path('delete_transaction/', views.delete_transaction, name='delete_transaction'),
    path('edit_transaction/<int:pk>/', views.edit_transaction, name='edit_transaction'),
    path('summary/', views.summary, name='summary'),
    path('get_portfolio_summary/', views.get_portfolio_summary, name='get_portfolio_summary'),
]