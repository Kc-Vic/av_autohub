from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from .models import Product, brand
from .forms import ProductForm

# Create your views here.
def all_products(request):
    
    products = Product.objects.all()
    query = None
    brands = None
    condition = None
    credit_available = None
    accessory_types = [],
    current_category = None,
    sort = None
    direction = None
    
    if request.GET:
    
    # --- DYNAMIC SORTING LOGIC ---
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            
            # Determine direction
            if 'direction' in request.GET:
                direction = request.GET['direction']
                desc_prefix = '-' if direction == 'desc' else ''
            else:
                desc_prefix = '-'
            current_category = request.GET.get('category')
            
            final_sort_key = None
            
            if current_category == 'Cars' or (current_category is None and products.filter(category='Cars').exists()):
                if sortkey == 'year':
                    # Order by Year (desc) then Price (desc)
                    final_sort_key = (f'{desc_prefix}year', f'{desc_prefix}price') 
                elif sortkey == 'price':
                    # Order by Price (desc/asc) then Year (as a secondary tie-breaker)
                    final_sort_key = (f'{desc_prefix}price', f'{desc_prefix}year') 

            elif current_category == 'Accessories' or current_category == 'Offers':
                # Accessories and Offers only sort by price.
                if sortkey == 'price':
                    final_sort_key = [f'{desc_prefix}price'] 
                    
            # Apply the final sort key
            if final_sort_key:
                products = products.order_by(*final_sort_key)
            
    # --- FILTERING LOGIC ---
        if 'category' in request.GET:
            category = request.GET['category']
            products = products.filter(category__iexact=category)
        if 'accessory_type' in request.GET:
            accessory_types = request.GET['accessory_type'].split(',')
            products = products.filter(accessory_type__in=accessory_types)
            accessory_types = accessory_types
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
    
    current_sorting = f'{sort}_{direction}'
    
    context = {
        'products': products,
        'search_term': query, 
        'current_brands': brands,
        'current_condition': condition,
        'current_credit_available': credit_available,
        'current_accessories_types': accessory_types,
        'current_category': current_category,
        'current_sorting': current_sorting,
    }
    
    return render(request, 'products/products.html', context)

def product_detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    
    context = {
        'product': product,
    }
    
    return render(request, 'products/product_detail.html', context)

def add_product(request):
    """ Add a product to the store """
    
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))
    
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
    
    template = 'products/add_product.html'
    context = {
        'form': form,
    }
    
    return render(request, template, context)