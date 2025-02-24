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


class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    area_of_interest = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    country = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))
    state = forms.CharField(max_length=100, required=True, widget=forms.TextInput(attrs={'class': 'text-black p-2 w-full'}))

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        # Pre-fill fields with user data
        if self.user:
            self.fields['username'].initial = self.user.username
            self.fields['email'].initial = self.user.email
            profile = getattr(self.user, 'profile', None)
            if profile:
                self.fields['age'].initial = profile.age
                self.fields['country'].initial = profile.country
                self.fields['state'].initial = profile.state
                self.fields['area_of_interest'].initial = profile.area_of_interest

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.exclude(pk=self.user.pk).filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.user.pk).filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
