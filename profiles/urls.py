from django.urls import path
from . import views

urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>', views.order_history, name='order_history'),
    path('credit_history/<application_id>', views.credit_history, name='credit_history'),
    path('delete/', views.delete_account, name='delete_account'),
]