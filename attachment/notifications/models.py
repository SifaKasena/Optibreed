from django.db import models
from optibreed.models import Room

# Create your models here.
class Notification(models.Model):
    STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read')
    ]

    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='unread')

    class Meta:
        ordering = ['-timestamp']