from django.contrib import admin
from .models import brand, Product

# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'brand', 'price', 'year', 'mileage', 'condition', 'credit_available')
    list_filter = ('brand', 'condition', 'credit_available', 'year', 'category', 'accessory_type')
    search_fields = ('title', 'brand__brand', 'price')
    
    ordering = ('-year', 'brand', 'title')
    
class BrandAdmin(admin.ModelAdmin):
    list_display = ('brand',)
    search_fields = ('brand',)

admin.site.register(brand, BrandAdmin)
admin.site.register(Product, ProductAdmin)