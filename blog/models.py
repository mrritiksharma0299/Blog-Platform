from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django_countries.fields import CountryField
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from cloudinary.models import CloudinaryField

CATEGORY_CHOICES = [
    ("Sports", "Sports"),
    ("Travel", "Travel"),
    ("Food", "Food"),
    ("Business", "Business"),
    ("Technology", "Technology"),
    ("Gaming", "Gaming"),
    ("Photography", "Photography"),
    ("Education", "Education"),
    ("Music", "Music"),
    ("Movies", "Movies"),
    ("Health", "Health"),
    ("Lifestyle", "Lifestyle"),
    ("Other", "Other"),
]


class Post(models.Model):

    VISIBILITY_CHOICES = [
        ("public", "Public"),
        ("followers", "Followers Only"),
        ("community", "Community"),
    ]

    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    title = models.CharField(
        max_length=200
    )

    country = CountryField(
        blank_label="Select Country"
    )

    category = models.CharField(
        max_length=100,
        choices=CATEGORY_CHOICES,
    )

    other_category = models.CharField(
        max_length=100,
        blank=True
    )

    visibility = models.CharField(
        max_length=20,
        choices=VISIBILITY_CHOICES,
        default="public",
    )

    community = models.ForeignKey(
        "community.Community",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="posts",
    )


    slug = models.SlugField(
        max_length=200,
        unique=True
    )

    content = models.TextField()

    featured_image = CloudinaryField(
        "image",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    published = models.BooleanField(
        default=True
    )

    @property
    def reading_time(self):
        words = len(self.content.split())
        minutes = max(1, words // 200)
        return f"{minutes} min read"
    
    @property
    def total_likes(self):
        return self.post_likes.count()
    
    @property
    def total_comments(self):
        return self.comments.count()
    
    
    
    class Meta:
        ordering = ["-created_at"]


    def save(self, *args, **kwargs):

        if not self.slug:

            slug = slugify(self.title)

            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{slugify(self.title)}-{get_random_string(5)}"

            self.slug = slug

        super().save(*args, **kwargs)


    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse(
            "blog_detail",
            kwargs={"slug": self.slug}
        )
    
class PostLike(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="liked_posts"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_likes"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_user_post_like",
            )
        ]

    def __str__(self):
        return f"{self.user.username} likes {self.post.title}"
    

class Comment(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="comments"
    )

    text = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.user.username} commented on {self.post.title}"