from django.shortcuts import render, redirect
from .forms import AdvertiserRegistrationForm
from account.models import User
from .models import Advertiser, Advertisements
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from .utils import check_malicious_url
# Create your views here.

def resister(request):
    if request.method == 'POST':
        form = AdvertiserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            confirm_password = request.POST.get('confirm_password')
            business_name = form.cleaned_data['business_name']
            business_type = form.cleaned_data['business_type']
            contact_number = form.cleaned_data['contact_number']
            address = form.cleaned_data['address']
            profile_image = form.cleaned_data['profile_image']

            user = User.objects.create_user(username=username, email=email, password=password, user_type='advertiser')
            Advertiser.objects.create(user=user, business_name=business_name, business_type=business_type, contact_number=contact_number, address=address, profile_image=profile_image)
            messages.success(request, 'Registration Successfull! please login')
            return redirect('login')
    else:
        form = AdvertiserRegistrationForm
    return render(request, 'advertisers/register.html', {'form': form})

@never_cache
@login_required
def add_advertisement(request):
    advertiser = Advertiser.objects.get(user=request.user)
    if request.method == 'POST':
        title = request.POST.get('title')
        link = request.POST.get('link')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        description = request.POST.get('description')
        advertisement_type = request.POST.get('advertisement_type')
        image = request.FILES.get('image')

        if title and link and start_date and end_date and description and advertisement_type and image:
            Advertisements.objects.create(
                advertiser=advertiser, 
                title=title,
                link=link,
                start_date=start_date,
                end_date=end_date,
                description=description,
                advertisement_type=advertisement_type,
                image=image
            )
            messages.success(request, "Advertisement added successfully!")
            return redirect('advertisers:add_advertisement')
        else:
            messages.error(request, "All fields are required.")

    return render(request, 'advertisers/add_advertisement.html')\

@never_cache
@login_required 
def view_advertisements(request):
    advertisements = Advertisements.objects.filter(advertiser=request.user.advertiser)
    return render(request, 'advertisers/view_advertisements.html', {'advertisements': advertisements})


def ad_click(request, ad_id):
    """
    Handles ad clicks, checks if the URL is malicious, and redirects the user accordingly.

    Args:
        request: The HTTP request object.
        ad_id (int): The ID of the clicked advertisement.

    Returns:
        Redirects to the ad URL or displays a warning.
    """
    ad = Advertisements.objects.get(id=ad_id)

    # Run ML model to check if the ad URL is safe
    result = check_malicious_url(ad.link)

    if result == "Benign":
        return redirect(ad.link)
    else:
        # If the ad is unsafe, show a warning message
        messages.error(request, f"Warning! This website is classified as {result}. Proceed with caution.")
        return render(request, "posts/ad_warning.html", {"ad": ad, "result": result})