from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from optibreed.models import Room
from .models import Notification

# Create your views here.
@login_required
def notifications_list(request):
    status = request.GET.get('status')
    date = request.GET.get('date')

    rooms = Room.objects.filter(User=request.user)
    notifications = Notification.objects.filter(Room__in=rooms)

    if status:
        notifications = notifications.filter(status=status)
    if date:
        notifications = notifications.filter(timestamp__date=date)

    context = {
        'notifications': notifications
    }

    return render(request, 'core/notifications/list.html', context)


@login_required
def notification_details(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    context = {
        'notification': notification
    }

    return render(request, 'core/notifications/detail.html', context)

@login_required
def notification_delete(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    notification.delete()

    return redirect('notifications:list')

@login_required
def notification_update_status(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)

    if notification.status == 'unread':
        notification.status = 'read'

    notification.save()

    return redirect('notifications:list')
