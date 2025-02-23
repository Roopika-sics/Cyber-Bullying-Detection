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
    return render(request, "posts/post_list.html", {"posts": posts})

@never_cache
@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like = Like.objects.filter(user=request.user, post=post).first()
    if like:
        like.delete()
    else:
        Like.objects.create(user=request.user, post=post)
        
    return redirect("home")

@never_cache
@login_required
def comment_on_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = post
            comment.save()
    return redirect("home")
