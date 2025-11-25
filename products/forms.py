from django import forms
from .models import Product, brand

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'brand', 'title', 'price', 'year', 'mileage', 
            'condition', 'credit_available', 'image', 
            'description', 'category', 'accessory_type'
        ]
        
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'brand': 'Brand',
            'title': 'Product Title',
            'price': 'Price',
            'year': 'Year',
            'mileage': 'Mileage',
            'condition': 'Condition',
            'credit_available': 'Credit Available',
            'image': 'Product Image',
            'description': 'Description',
            'category': 'Category',
            'accessory_type': 'Accessory Type',
        }

        self.fields['brand'].widget.attrs['autofocus'] = True
        for field in self.fields:
            placeholder = placeholders[field]
            self.fields[field].widget.attrs['class'] = 'form-control rounded-0'
            #self.fields[field].widget.attrs['placeholder'] = placeholder
            #self.fields[field].label = False