from django.contrib import admin
from django.contrib.auth import get_user_model
from apps.post.models import Post

UserProfile = get_user_model()


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'body')

# Register your models here.
