from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .forms import OrderForm  # Make sure checkout/forms.py exists and defines OrderForm
from products.models import Product # Import the Product model

def checkout_view(request, product_id):
    
    # Get the product the user wants to buy
    product = get_object_or_404(Product, pk=product_id)

    # Calculate totals (assuming quantity is 1)
    order_total = product.price
    grand_total = order_total

    # We assume the POST logic will be here later
    # For a GET request, just create an empty form
    order_form = OrderForm()
    
    context = {
        'order_form': order_form,
        'product': product,         # Pass the product to the template
        'order_total': order_total,   # Pass the total to the template
        'grand_total': grand_total, # Pass the total to the template
    }
    
    return render(request, 'checkout/checkout.html', context)