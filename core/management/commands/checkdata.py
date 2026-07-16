from django.core.management.base import BaseCommand
from blog.models import Post
from django.contrib.auth.models import User


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        print("Posts:", Post.objects.count())
        print("Users:", User.objects.count())