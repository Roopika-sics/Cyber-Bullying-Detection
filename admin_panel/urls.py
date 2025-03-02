from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('users/', views.all_users, name='all_users'),
    path('posts/', views.all_posts, name='all_posts'),
    path('delete-post/<int:post_id>/', views.delete_post, name='delete_post')
    
]
