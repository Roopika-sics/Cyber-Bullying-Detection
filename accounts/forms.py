from django import forms
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    area_of_interest = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField()
    country = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if User.objects.filter(username=username).exists():
            self.add_error('username', 'Username already exists.')

        if User.objects.filter(email=email).exists():
            self.add_error('email', 'Email is already registered.')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match.')

        return cleaned_data
