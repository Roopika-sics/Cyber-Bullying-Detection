from django.contrib import admin
from . models import Post,Like,Comment
# Register your models here.


class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'content', 'image', 'created_at')

admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)
