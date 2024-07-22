# notification/context_processors.py

from .models import Notification
from optibreed.models import Room

def notification_context(request):
    if request.user.is_authenticated:
        rooms = Room.objects.filter(User=request.user)
        notifications = Notification.objects.filter(Room__in=rooms)
        return {
            'notifications': notifications
        }
    return {}
