from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .forms import RegistrationForm
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
import random
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import OTP

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')
            area_of_interest = form.cleaned_data['area_of_interest']
            age = form.cleaned_data['age']
            country = form.cleaned_data['country']
            state = form.cleaned_data['state']
            
            user = User.objects.create_user(username=username, email=email, password=password)
            Profile.objects.create(user=user, area_of_interest=area_of_interest, age=age, country=country, state=state)

            messages.success(request, 'Registration Successfull! please login')
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
            return redirect("landing")
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, "accounts/login.html")


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            otp_code = str(random.randint(100000, 999999))  
            OTP.objects.create(user=user, otp=otp_code)

            # Send email
            send_mail(
                "Password Reset OTP",
                f"Your OTP for password reset is: {otp_code}",
                "your_email@example.com",
                [email],
                fail_silently=False,
            )
            request.session["reset_email"] = email
            return redirect("verify_otp")
        except User.DoesNotExist:
            messages.error(request, "Email not found")

    return render(request, "accounts/forgot_password.html")

def verify_otp(request):
    if request.method == "POST":
        email = request.session.get("reset_email")
        entered_otp = request.POST.get("otp")

        try:
            user = User.objects.get(email=email)
            otp_entry = OTP.objects.filter(user=user).order_by("-created_at").first()

            if otp_entry and otp_entry.otp == entered_otp:
                request.session["otp_verified"] = True
                return redirect("reset_password")
            else:
                messages.error(request, "Invalid OTP")
        except User.DoesNotExist:
            messages.error(request, "User not found")

    return render(request, "accounts/verify_otp.html")

def reset_password(request):
    if not request.session.get("otp_verified"):
        return redirect("forgot_password")

    if request.method == "POST":
        email = request.session.get("reset_email")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if new_password == confirm_password:
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Password reset successful! Please login.")
                del request.session["reset_email"]
                del request.session["otp_verified"]
                return redirect("login")
            except User.DoesNotExist:
                messages.error(request, "User not found")
        else:
            messages.error(request, "Passwords do not match")

    return render(request, "accounts/reset_password.html")


@login_required(login_url='login')
def dashboard(request):
    return render(request, "accounts/dashboard.html")

def user_logout(request):
    logout(request)
    return redirect("login")
