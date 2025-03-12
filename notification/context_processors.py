from .models import Notification

def unread_notifications_count(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': request.user.notifications.filter(is_read=False).count()
        }
    return {}