from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import re

class AdvertiserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    business_name = forms.CharField(max_length=255)
    business_type = forms.CharField(max_length=255)
    contact_number = forms.CharField(max_length=20)
    address = forms.CharField(max_length=255)
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
