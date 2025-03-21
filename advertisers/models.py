from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Advertiser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    business_name = models.CharField(max_length=255)
    business_type = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    profile_image = models.ImageField(upload_to='advertiser_profiles/', null=True, blank=True)

    def __str__(self):
        return self.business_name