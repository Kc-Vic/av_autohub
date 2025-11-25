from django.urls import path
from . import views
from .webhooks import webhook

urlpatterns = [
    path('<int:product_id>/', views.checkout_view, name='checkout'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('wh/', webhook, name='webhook'),
]