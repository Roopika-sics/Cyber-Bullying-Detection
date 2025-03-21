from django.urls import path
from . import views

app_name = 'advertisers'

urlpatterns = [
    path('register/', views.resister, name='register'),
    path('add-advertisement/', views.add_advertisement, name='add_advertisement'),
    path('view-advertisements/', views.view_advertisements, name='view_advertisements'),

]
