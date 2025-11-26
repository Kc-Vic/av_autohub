from django.db import models

# Create your models here.
class aboutUs(models.Model):
    
    class Meta:
        verbose_name_plural = "About Us"

    title = models.CharField(max_length=200)
    profile = models.ImageField(upload_to='about_profiles/', null=True, blank=True)
    locations = models.TextField()
    content = models.TextField()
    

    def __str__(self):
        return self.title
    
class team(models.Model):
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='team_photos/')
    bio = models.TextField()

    def __str__(self):
        return self.name