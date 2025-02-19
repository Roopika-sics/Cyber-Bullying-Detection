from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    area_of_interest = models.CharField(max_length=255, blank=True)
    age = models.IntegerField(null=True)
    country = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"