from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify




class Community(models.Model):

    name = models.CharField(
        max_length=100,
        unique=True
    )

    slug = models.SlugField(
        unique=True,
        blank=True
    )

    description = models.TextField()

    image = models.ImageField(
        upload_to="community/",
        blank=True,
        null=True
    )

    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="created_communities"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def save(self, *args, **kwargs):

        if not self.slug:
            self.slug = slugify(self.name)

        super().save(*args, **kwargs)


    def total_members(self):

        return self.members.count()


    def get_initial(self):

        return self.name[0].upper()


    def __str__(self):

        return self.name
    
    
class Membership(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="members"
    )

    joined_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        unique_together = (
            "user",
            "community",
        )


    def __str__(self):

        return f"{self.user.username} - {self.community.name}"
    


class CommunityMessage(models.Model):

    community = models.ForeignKey(
        Community,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    message = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.sender.username} - {self.community.name}"
    

