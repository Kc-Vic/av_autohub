from django.db import models

# Create your models here.

class brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand
    
class Product(models.Model):
    
    ACCESSORY_TYPES = [
        ('Internal', 'Internal'),
        ('External', 'External'),
        ('Engine', 'Engine'),
        ('Others', 'Others'),
    ]
    
    CATEGORY = [
        ('Cars', 'Cars'),
        ('Accessories', 'Accessories'),
    ]
    
    CONDITION = [
        ('New', 'New'),
        ('Used', 'Used'),
    ]
    
    brand = models.ForeignKey(
        brand, null=True, blank=True,
        on_delete=models.SET_NULL, related_name='products'
    )
    title = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=20, decimal_places=0)
    year = models.PositiveIntegerField(blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        choices=CONDITION, 
        default='Used'
    )
    credit_available = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    category = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        choices=CATEGORY, 
        default='Cars'
    )
    accessory_type = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        choices=ACCESSORY_TYPES, 
        default='Others'
    )

    def __str__(self):
        return self.title