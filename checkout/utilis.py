from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

# Note: You need to import the Order model if it's not defined in the same file.
# Assuming Order model is in your models.py file:
# from .models import Order 

def send_confirmation_email(order):
    """
    Sends a confirmation email to the user after a successful payment.
    """
    customer_email = order.email
    subject = f'Your Order Confirmation - Order No. {order.order_number}'
    
    # Render Email Body Templates
    body = render_to_string(
        'checkout/emails/confirmation_email_body.txt',
        {'order': order}
    )
    
    html_body = render_to_string(
        'checkout/emails/confirmation_email_body.html',
        {'order': order}
    )

    # Send the Email
    send_mail(
        subject,
        body,
        settings.DEFAULT_FROM_EMAIL,
        [customer_email],
        fail_silently=False,
        html_message=html_body,
    )