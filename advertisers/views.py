from django.shortcuts import render, redirect
from .forms import AdvertiserRegistrationForm
from django.contrib.auth.models import User
from .models import Advertiser
from django.contrib import messages
# Create your views here.

def resister(request):
    if request.method == 'POST':
        form = AdvertiserRegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')
            business_name = form.cleaned_data['business_name']
            business_type = form.cleaned_data['business_type']
            contact_number = form.cleaned_data['contact_number']
            address = form.cleaned_data['address']

            user = User.objects.create_user(username=username, email=email, password=password)
            Advertiser.objects.create(user=user, business_name=business_name, business_type=business_type, contact_number=contact_number, address=address)
            messages.success(request, 'Registration Successfull! please login')
            return redirect('login')
    else:
        form = AdvertiserRegistrationForm
    return render(request, 'advertisers/register.html')