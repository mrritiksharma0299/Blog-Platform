from django.db import models
from django.contrib.auth.models import User

from blog.models import Post


class Notification(models.Model):

    NOTIFICATION_TYPES = (

        ("follow", "Follow"),

        ("blog", "Blog"),

        ("like", "Like"),

        ("comment", "Comment"),

        ("community", "Community"),

    )


    receiver = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="notifications"
    )


    sender = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )


    notification_type = models.CharField(
        max_length=20,
        choices=NOTIFICATION_TYPES
    )


    message = models.CharField(
        max_length=255
    )

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )



    url_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )


    is_read = models.BooleanField(
        default=False
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:

        ordering = [
            "-created_at"
        ]


    def __str__(self):

        return f"{self.sender.username} → {self.receiver.username}"