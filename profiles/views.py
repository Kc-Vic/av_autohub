from django.shortcuts import render, get_object_or_404
from .models import UserProfile

# Create your views here.
def profile(request):
    profiles = get_object_or_404(UserProfile, user=request.user)
    context = {
        'profiles': profiles,
    }
    return render(request, 'profiles/profiles.html', context)