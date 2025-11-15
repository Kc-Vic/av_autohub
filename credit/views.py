from django.shortcuts import render

# Create your views here.
def credit_application(request):
    return render(request, 'credit/application.html')

def credit_options(request):
    return render(request, 'credit/credit_options.html')