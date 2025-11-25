from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import userProfileForm

from checkout.models import Order
from credit.models import CreditApplication
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        form = userProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
    
    form = userProfileForm(instance=profile)
    orders = profile.orders.all()
    
    context = {
        'form': form,
        'orders': orders,
        'credit_applications': request.user.credit_applications.all().order_by('-created_at'),
        'on_profile_page': True,
    }
    return render(request, 'profiles/profile.html', context)

def order_history(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/payment_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)

@login_required
def credit_history(request, application_id):
    credit_applications = request.user.credit_applications.all().order_by('-created_at')
    template = 'profiles/profile.html'
    context = {
        'form': form,
        'orders': orders,
        # Passing both history QuerySets to the template
        'credit_applications': credit_applications,
        'on_profile_page': True 
    }
    
    return render(request, template, context)