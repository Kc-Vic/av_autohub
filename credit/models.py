import uuid

from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Model 1: The main application
class CreditApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    # Link to the user who is applying
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="credit_applications")
    
    # Form fields
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    job_business_title = models.CharField(max_length=255)
    employer_business_address = models.TextField()
    annual_income = models.DecimalField(max_digits=15, decimal_places=0) # Use 0 for whole Naira

    # Admin/Tracking fields
    application_id = models.CharField(max_length=20, unique=True, editable=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _generate_application_id(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()
    
    def save(self, *args, **kwargs):

        if not self.application_id:
            self.application_id = self._generate_application_id()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.application_id

    def __str__(self):
        return f"Application for {self.full_name} ({self.status})"

# Model 2: The supporting files
class SupportingDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('ID', 'Proof of ID'),
        ('Address', 'Proof of Address'),
        ('Income', 'Proof of Income'),
    ]

    # Link to the application
    application = models.ForeignKey(CreditApplication, on_delete=models.CASCADE, related_name="documents")
    
    # The file itself
    document = models.FileField(upload_to='credit_documents/')
    document_type = models.CharField(max_length=10, choices=DOCUMENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.get_document_type_display()} for {self.application.full_name}"