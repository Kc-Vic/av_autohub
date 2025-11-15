from django.urls import path
from . import views

urlpatterns = [
    path('options/', views.credit_options, name='credit_options'),
    path('application/', views.credit_application, name='credit_application'),
]