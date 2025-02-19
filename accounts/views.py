from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            area_of_interest = form.cleaned_data['area_of_interest']
            age = form.cleaned_data['age']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, area_of_interest=area_of_interest, age=age, country=country, state=state)
            return redirect('login')  
    else:
        form = RegistrationForm()

    return render(request, "accounts/register.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, "accounts/login.html")

@login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")

def user_logout(request):
    logout(request)
    return redirect("login")
