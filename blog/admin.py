from django.contrib import admin
from .models import Post, PostLike, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):

    list_display = (
        "title",
        "author",
        "country",
        "total_likes",
        "total_comments",
        "created_at",
        "published",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "post",
        "created_at",
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "post",
        "created_at",
    )