import requests
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import json

@require_POST
@csrf_exempt
def paypal_webhook(request):
    """
    Listens for webhooks from PayPal and verifies their authenticity.
    """
    try:
        payload = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponse(status=400, content='Invalid JSON payload')
    
    if settings.PAYPAL_LIVE_MODE:
        paypal_url = 'https://ipnpb.paypal.com/cgi-bin/webscr'
    else:
        paypal_url = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'
        
    verification_data = {'cmd': '_notify-validate'}

    try:
        # Create a new HTTP request back to PayPal with the original data + verification command
        response = requests.post(paypal_url, data=payload, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status() # Raise exception for bad status codes
    except requests.exceptions.RequestException as e:
        # Network or connection error while trying to talk back to PayPal
        print(f"PayPal Verification Error: {e}")
        return HttpResponse(status=500, content='PayPal verification failed')

    if response.text == 'VERIFIED':

        return HttpResponse(status=200, content='VERIFIED')

    elif response.text == 'INVALID':
        # Authentication failed
        print(f"PayPal Webhook Verification failed: INVALID response.")
        return HttpResponse(status=400, content='Invalid PayPal notification')
        
    else:
        # Unknown response
        print(f"PayPal Webhook Verification received unknown response: {response.text}")
        return HttpResponse(status=400, content='Unknown PayPal response')