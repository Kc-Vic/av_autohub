from django.shortcuts import render, get_object_or_404
from products.models import Product  # Import your Product model
from decimal import Decimal

# Create your views here.
def credit_application(request):
    return render(request, 'credit/application.html')

def credit_options_view(request, product_id):
    """ A view to show credit options for a specific product """
    product = get_object_or_404(Product, pk=product_id)

    # 1. Calculate the payments
    down_payment = product.price * Decimal('0.50')
    remaining_balance = product.price - down_payment

    # 2. Create the list of options
    options = [
        {
            'duration': 6,
            'payment': remaining_balance / 6
        },
        {
            'duration': 12,
            'payment': remaining_balance / 12
        },
        {
            'duration': 18,
            'payment': remaining_balance / 18
        },
    ]

    # 3. Define the context to send to the template
    context = {
        'product': product,
        'down_payment': down_payment,
        'options': options,
    }

    return render(request, 'credit/credit_options.html', context)