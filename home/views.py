from django.shortcuts import render
from .models import aboutUs, team
from django.contrib import admin

# Create your views here.

def index(request):
    
    return render(request, 'home/index.html')

def about(request):
    
    company_info = aboutUs.objects.first()
    team_members = team.objects.all()
    
    context = {
        'company_info': company_info,
        'team_members': team_members
    }
    
    return render(request, 'home/about.html', context)
