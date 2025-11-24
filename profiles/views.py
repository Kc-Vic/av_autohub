from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from .models import UserProfile
from .forms import userProfileForm

# Create your views here.
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
        'on_profile_page': True,
    }
    return render(request, 'profiles/profile.html', context)