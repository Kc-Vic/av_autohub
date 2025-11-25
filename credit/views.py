from django.shortcuts import render, redirect, get_object_or_404
from products.models import Product  # Import your Product model
from decimal import Decimal
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # <-- ADD THIS LINE
from .models import CreditApplication, SupportingDocument
from .forms import CreditApplicationForm

# Create your views here.

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

# view for credit application form
@login_required # Make sure the user is logged in to apply
def credit_application_view(request):
    """ A view to handle the credit application submission """
    
    if request.method == 'POST':
        form = CreditApplicationForm(request.POST)

        # Get the file lists from the request
        id_files = request.FILES.getlist('proof_of_id')
        address_files = request.FILES.getlist('proof_of_address')
        income_files = request.FILES.getlist('proof_of_income')

        # Check if files were uploaded and form is valid
        if form.is_valid() and id_files and address_files and income_files:
            
            # 1. Save the main application form
            application = form.save(commit=False)
            application.user = request.user # Link to the logged-in user
            application.save() # Save application to get its ID

            # 2. Create SupportingDocument objects for each uploaded file
            for f in id_files:
                SupportingDocument.objects.create(
                    application=application,
                    document=f,
                    document_type='ID'
                )
            for f in address_files:
                SupportingDocument.objects.create(
                    application=application,
                    document=f,
                    document_type='Address'
                )
            for f in income_files:
                SupportingDocument.objects.create(
                    application=application,
                    document=f,
                    document_type='Income'
                )
            
            messages.success(request, 'Your application has been submitted! We will contact you shortly.')
            return redirect('profile') # Redirect to home page after success
        
        else:
            messages.error(request, 'Please correct the errors below and ensure you have uploaded documents for all categories.')

    else: # if a GET request
        form = CreditApplicationForm()

    context = {
        'form': form,
    }
    return render(request, 'credit/application.html', context)

@login_required
def credit_application_detail_view(request, application_id):
    """
    Shows the status page for a single credit application.
    The template rendered is dynamically chosen based on the application's status.
    """
    
    # Securely retrieve the application, ensuring it belongs to the logged-in user
    application = get_object_or_404(
        CreditApplication, 
        application_id=application_id,
        user=request.user
    )
    
    # Determine the template based on the status
    if application.status == 'Approved':
        template_name = 'credit/credit_approved.html'
    elif application.status == 'Rejected':
        template_name = 'credit/credit_denied.html'
    else: # 'Pending' or any other status
        template_name = 'credit/credit_pending.html'
        
    context = {
        'application': application
    }
    
    return render(request, template_name, context)