from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, brand

# Create your views here.
def all_products(request):
    
    products = Product.objects.all()
    query = None
    brands = None
    condition = None
    credit_available = None
    if request.GET:    
        if 'brand' in request.GET:
            brands = request.GET['brand'].split(',')
            products = products.filter(brand__brand__in=brands)
            brands = brand.objects.filter(brand__in=brands)
        if 'condition' in request.GET:
            condition = request.GET['condition']
            products = products.filter(condition__iexact=condition)
        if 'credit_available' in request.GET:
            credit_available = request.GET['credit_available']
            if credit_available == 'True':
                products = products.filter(credit_available=True)
            elif credit_available == 'False':
                products = products.filter(credit_available=False)
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            queries = Q(title__icontains=query) | Q(description__icontains=query) | Q(year__icontains=query) |  Q(condition__icontains=query) 
            products = products.filter(queries)
    
    
    context = {
        'products': products,
        'search_term': query, 
        'current_brands': brands,
        'current_condition': condition,
        'current_credit_available': credit_available,
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)