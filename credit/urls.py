from django.urls import path
from . import views

urlpatterns = [
    path('<int:product_id>/', views.credit_options_view, name='credit_options'),
    path('application/', views.credit_application_view, name='credit_application'),
]