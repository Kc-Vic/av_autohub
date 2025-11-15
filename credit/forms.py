from django import forms
from .models import CreditApplication

class CreditApplicationForm(forms.ModelForm):
    class Meta:
        model = CreditApplication
        # We only want the fields the user needs to fill out
        fields = (
            'full_name', 
            'address', 
            'job_business_title', 
            'employer_business_address', 
            'annual_income'
        )

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and labels.
        """
        super().__init__(*args, **kwargs)
        
        placeholders = {
            'full_name': 'Your full name as it appears on your ID',
            'address': 'Your current residential address',
            'job_business_title': 'Your Job Title or Business Name',
            'employer_business_address': 'The full address of your employer or business',
            'annual_income': 'Your total annual income (e.g., 5000000)',
        }
        
        self.fields['annual_income'].label = "Annual Income (₦)"

        for field_name, placeholder in placeholders.items():
            self.fields[field_name].widget.attrs['placeholder'] = placeholder
            # You can add the 'form-control' class here if you're not using crispy-forms
            self.fields[field_name].widget.attrs['class'] = 'form-control rounded-0'