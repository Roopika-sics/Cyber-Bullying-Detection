from django import forms
from account.models import User
from django.core.exceptions import ValidationError
import re
from .models import Advertiser
class AdvertiserRegistrationForm(forms.ModelForm):
    username = forms.CharField(
        max_length=150, 
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )
    business_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Name'})
    )
    business_type = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Business Type'})
    )
    contact_number = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Contact Number'})
    )
    address = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'})
    )
    profile_image = forms.ImageField(
        required=True, 
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Advertiser
        fields = ['username', 'email', 'password', 'confirm_password', 'business_name', 'business_type', 'contact_number', 'address', 'profile_image']

        
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise ValidationError("Username already exists.")
        return username
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data
    

class EditAdvertiserForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    business_name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    business_type = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    contact_number = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    address = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'class': 'text-black p-2 w-full'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

       
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            advertiser = getattr(self.user, 'advertiser', None)
            if advertiser:
                self.fields['business_name'].initial = advertiser.business_name
                self.fields['business_type'].initial = advertiser.business_type
                self.fields['contact_number'].initial = advertiser.contact_number
                self.fields['address'].initial = advertiser.address
                self.fields['profile_image'].initial = advertiser.profile_image
