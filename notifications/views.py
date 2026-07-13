from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from notifications.models import Notification
from accounts.models import Follow

@login_required
def notification_list(request):

    notifications = request.user.notifications.all()

    Notification.objects.filter(
        receiver=request.user,
        is_read=False
    ).update(is_read=True)

    return render(
        request,
        "notifications/list.html",
        {
            "notifications": notifications
        }
    )