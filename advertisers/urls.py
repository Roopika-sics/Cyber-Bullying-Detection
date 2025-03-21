from django.urls import path
from . import views

app_name = 'advertisers'

urlpatterns = [
    path('register/', views.resister, name='register'),
]
