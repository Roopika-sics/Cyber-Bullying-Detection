from django.urls import path
from .views import create_post, post_list, like_post, comment_on_post

urlpatterns = [
    path("", post_list, name="home"),
    path("create/", create_post, name="create_post"),
    path("like/<int:post_id>/", like_post, name="like_post"),
    path("comment/<int:post_id>/", comment_on_post, name="comment_post"),
]
