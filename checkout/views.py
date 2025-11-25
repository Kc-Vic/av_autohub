import requests
import hmac
import hashlib
import json
import os
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.urls import reverse
from .forms import OrderForm
from .models import Order, OrderLineItem
from products.models import Product
from decimal import Decimal
from decimal import ROUND_HALF_UP
from profiles.models import UserProfile
from profiles.forms import userProfileForm
from .utilis import send_confirmation_email

"""
The `checkout_view` function handles the checkout process for a product, including form validation,
preparing data for payment processing with Paystack, and redirecting to Paystack for payment
authorization.

:param request: The `request` parameter in Django represents the HTTP request that was sent to the
view. It contains information about the request, such as the user making the request, any data sent
with the request (POST data), the method used (GET, POST, etc.), and more. The view uses this
:param product_id: The `product_id` parameter in the `checkout_view` function is used to identify
the specific product that the user is trying to purchase. It is retrieved from the URL and then used
to fetch the corresponding product object from the database using Django's `get_object_or_404`
function. This ensures
:return: The `checkout_view` function returns a rendered template 'checkout/checkout.html' with the
context data containing the order form, product details, order total, grand total, and Paystack
public key.
"""


def checkout_view(request, product_id):
    
    product = get_object_or_404(Product, pk=product_id)
    safe_price = product.price.quantize(Decimal('1'), rounding=ROUND_HALF_UP)

    order_total = product.price
    grand_total = order_total
    
    order_form = None
    
    if request.method == 'POST':
        form = OrderForm(request.POST)

        if form.is_valid():
            # Form is valid, but DON'T save to DB yet.
            # Save the form data and product_id to the session
            save_info = 'save-info' in request.POST
            
            request.session['pending_order'] = {
                'form_data': request.POST,
                'product_id': product_id,
                'save_info': save_info, 
            }

            # Prepare data to send to Paystack
            url = "https://api.paystack.co/transaction/initialize"
            email = form.cleaned_data.get('email')
            # Convert price to Kobo (Paystack requires integer)
            amount = int(safe_price * 100) 
            
            # The URL Paystack will redirect to after payment
            callback_url = request.build_absolute_uri(reverse('verify_payment'))
            
            headers = {
                "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
            }
            data = {
                "email": email,
                "amount": amount,
                "callback_url": callback_url,
            }

            # Make the API call
            r = requests.post(url, headers=headers, json=data)
            response = r.json()

            # If the request was successful, redirect to Paystack's page
            if response.get('status') == True:
                auth_url = response['data']['authorization_url']
                return redirect(auth_url)
            else:
                # API call failed
                messages.error(request, 'Could not connect to payment service. Please try again.')
                order_form = form
        else:
            # Form is invalid
            messages.error(request, 'Please correct the errors below.')
            order_form = form

    else: # GET request
        order_form = OrderForm()
        
    context = {
        'order_form': order_form,
        'product': product,         # Pass the product to the template
        'order_total': order_total,   # Pass the total to the template
        'grand_total': grand_total, # Pass the total to the template
        'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY,
    }
    
    return render(request, 'checkout/checkout.html', context)

def verify_payment(request):
    """
    Verify the payment with Paystack
    """
    # Get the payment reference from the URL
    reference = request.GET.get('trxref')
    if not reference:
        messages.error(request, 'No payment reference found.')
        return redirect('home')

    # Paystack API URL to verify a transaction
    url = f"https://api.paystack.co/transaction/verify/{reference}"

    # Set the authorization header
    headers = {
        "authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}"
    }

    # Make the request to Paystack
    r = requests.get(url, headers=headers)
    response = r.json()
    
    print(f"Paystack API Response: {response}")

    if response['status'] == True and response['data']['status'] == 'success':
        # Payment was successful

        # Retrieve the pending order from the session
        pending_order_data = request.session.get('pending_order')
        if not pending_order_data:
            messages.error(request, 'Session expired or invalid. Could not find order.')
            return redirect('home')

        product_id = pending_order_data.get('product_id')
        form_data = pending_order_data.get('form_data')
        save_info = pending_order_data.get('save_info', False) 
        product = get_object_or_404(Product, pk=product_id)
        paystack_amount_kobo = response['data']['amount']
        verified_total = Decimal(paystack_amount_kobo) / Decimal(100).quantize(Decimal('1'), rounding=ROUND_HALF_UP)

        # Create the Order in the database
        order = Order(
            full_name=form_data.get('full_name'),
            email=form_data.get('email'),
            phone_number=form_data.get('phone_number'),
            street_address1=form_data.get('street_address1'),
            street_address2=form_data.get('street_address2'),
            town_or_city=form_data.get('town_or_city'),
            state=form_data.get('state'),
            country=form_data.get('country'),
            postcode=form_data.get('postcode'),
            order_total=verified_total,
            grand_total=verified_total,
        )
        
        if request.user.is_authenticated:
            try:
                profile = UserProfile.objects.get(user=request.user)
                order.user_profile = profile
        
                if save_info:
                    profile_data = {
                        'default_phone_number': form_data.get('phone_number'),
                        'default_street_address1': form_data.get('street_address1'),
                        'default_street_address2': form_data.get('street_address2'),
                        'default_town_or_city': form_data.get('town_or_city'),
                        'default_state': form_data.get('state'),
                        'default_country': form_data.get('country'),
                        'default_postcode': form_data.get('postcode'),
                    }
                    user_profile_form = userProfileForm(profile_data, instance=profile)
                    if user_profile_form.is_valid():
                        user_profile_form.save()
            except UserProfile.DoesNotExist:
                pass
        order.save()

        # Create the OrderLineItem
        OrderLineItem.objects.create(
            order=order,
            product=product,
            quantity=1,
            lineitem_total=verified_total, 
        )
        try:
            send_confirmation_email(order)
        except Exception as e:
            print(f"Error sending email for order {order.order_number}: {e}")

        # Clean up the session
        del request.session['pending_order']

        messages.success(request, f"Payment successful! Your order number is {order.order_number}.")
        return render(request, 'checkout/payment_success.html', {'order': order})
    else:
        # Payment failed
        messages.error(request, 'Payment failed. Please try again.')
        return render(request, 'checkout/payment_failed.html')
    
def process_successful_payment(reference):
    """
    Looks up the payment reference, finalizes the order in the DB, 
    and returns the created Order object.
    """
    try:
        order = Order.objects.get(paystack_reference=reference)
        order.is_paid = True
        order.save()
        end_confirmation_email(order)
        
        return True
    except Order.DoesNotExist:
        print(f"Error: Order with reference {reference} not found.")
        return False
    except Exception as e:
        print(f"Unexpected error processing payment for reference {reference}: {e}")
        return False
    
@csrf_exempt
def paystack_webhook(request):
    
    PAYSTACK_SECRET = os.environ.get('PAYSTACK_SECRET_KEY')
    signature = request.headers.get('HTTP_X_PAYSTACK_SIGNATURE')
    payload = request.body
    
    calculated_signature = hmac.new(
        key=PAYSTACK_SECRET.encode('utf-8'),
        msg=payload,
        digestmod=hashlib.sha512
    ).hexdigest()
    
    if calculated_signature != signature:
        return HttpResponse(status=400, content='Invalid signature')
    
    try:
        event = json.loads(payload)
    except json.JSONDecodeError:
        return HttpResponse(status=400, content='Invalid JSON')
    
    if event['event'] == 'charge.success':
        reference = event['data']['reference']
        
        success = process_successful_payment(reference)
        
        if success:

            return HttpResponse(status=200, content='Success')
        else:

            return HttpResponse(status=200, content='Processing failed internally')
            
    return HttpResponse(status=200, content='Event received')