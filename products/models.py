from django.db import models

# Create your models here.

class brand(models.Model):
    brand = models.CharField(max_length=100)

    def __str__(self):
        return self.brand
    
class Product(models.Model):
    brand = models.ForeignKey(brand, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=50)
    year = models.PositiveIntegerField(blank=True, null=True)
    mileage = models.PositiveIntegerField(blank=True, null=True)
    condition = models.CharField(max_length=50, blank=True, null=True, choices=[('New', 'New'), ('Used', 'Used')], default='Used')
    credit_available = models.BooleanField(default=False)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title