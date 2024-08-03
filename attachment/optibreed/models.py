from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils import timezone

class Room(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Material_name = models.CharField(max_length=50)
    Min_Temperature = models.FloatField()
    Max_Temperature = models.FloatField()
    Min_Humidity = models.FloatField()
    Max_Humidity = models.FloatField()
    Min_Voltage = models.FloatField(default=0.0)
    Max_Voltage = models.FloatField(default=0.0)
    Door_Open = models.BooleanField(default=False)
    Door_Open_Timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.Material_name

    def door_open_duration(self):
        if self.Door_Open and self.Door_Open_Timestamp:
            return (timezone.now() - self.Door_Open_Timestamp).total_seconds() / 60  # duration in minutes
        return 0

class Sensor(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Sensor_type = models.CharField(max_length=50)
    Sensor_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Sensor_name} ({self.Sensor_type}) in {self.Room}"

class Condition(models.Model):
    DOOR_CONDITION_CHOICES = [
        ('Open', 'Open'),
        ('Closed', 'Closed'),
    ]
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField(default=timezone.now)
    Temperature = models.FloatField()
    Humidity = models.FloatField()
    Voltage = models.FloatField(default=0.0)
    DoorCondition = models.CharField(max_length=10, choices=DOOR_CONDITION_CHOICES, default="Closed")

    def __str__(self):
        return f'{self.Room.Material_name} at {self.Timestamp}'

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pics', default='profile.png')
    job_title = models.CharField(max_length=100, blank=True)
    twitter = models.URLField(blank=True)
    facebook = models.URLField(blank=True)
    instagram = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    about = models.TextField(blank=True)
    company = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    address = models.CharField(max_length=100)
    phone_number = PhoneNumberField(blank=True, null=True)
    email_notification = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.user.username} Profile'
