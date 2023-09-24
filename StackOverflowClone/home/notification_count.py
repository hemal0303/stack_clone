from blogs.models import Notification
from django.contrib.auth.decorators import login_required


def notification_count(request):
    try:
        unread_notifications_count = 0
        if request.user.is_authenticated:
            unread_notifications_count = Notification.objects.filter(
                receiver_id=request.user.id, is_read=False
            ).count()
        return {"notification_count": unread_notifications_count}

    except Exception as e:
        print("Error", e)
