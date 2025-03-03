from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from posts.models import Post, Comment

# Create your views here.

def is_admin(user):
    return user.is_superuser

@user_passes_test(is_admin)
def admin_dashboard(request):
    return render(request, 'admin_panel/admin_dashboard.html')

@login_required
@user_passes_test(is_admin)
def all_users(request):
    users = User.objects.all()
    return render(request, 'admin_panel/all_users.html', {'users':users})

@login_required
@user_passes_test(is_admin)
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'admin_panel/all_posts.html', {'posts': posts})

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user.is_superuser:
        post.delete()
        messages.success(request, "Post deleted successfully.")
    return redirect('all_posts')

def abusive_comments(request):
    flagged_comments = Comment.objects.filter(flagged=True)
    reported_comments = Comment.objects.filter(reported=True)
    return render(request, 'admin_panel/abusive_comments.html', {'flagged_comments': flagged_comments, 'reported_comments': reported_comments})

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.delete()
    return redirect('abusive_comments')