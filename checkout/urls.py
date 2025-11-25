from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('<int:product_id>/', views.checkout_view, name='checkout'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    ppath('paystack-webhook/', views.paystack_webhook, name='paystack_webhook'),
]