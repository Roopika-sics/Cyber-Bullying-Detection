from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Like, Comment
from .forms import PostForm, CommentForm
from django.views.decorators.cache import never_cache

@never_cache
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect("home")
    else:
        form = PostForm()
    return render(request, "posts/create_post.html", {"form": form})

@never_cache
@login_required
def post_list(request):
    posts = Post.objects.all().order_by("-created_at")

    for post in posts:
        post.is_liked_by_user = post.likes.filter(user=request.user).exists()

    return render(request, "posts/post_list.html", {"posts": posts})

@never_cache
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if not created:
        like.delete()
        liked = False
    else:
        liked = True
   
    return JsonResponse({"liked": liked, "likes_count": post.likes.count()})

@never_cache
@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        text = request.POST.get("text")

        if text:
            comment = Comment.objects.create(user=request.user, post=post, text=text)
            return JsonResponse({
                "success": True,
                "comment_id": comment.id,
                "username": comment.user.username,
                "text": comment.text,
            })
    
    return JsonResponse({"success": False}, status=400)