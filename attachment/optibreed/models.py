from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Material_name = models.CharField(max_length=50)
    Min_Temperature = models.FloatField()
    Max_Temperature = models.FloatField()
    Min_Humidity = models.FloatField()
    Max_Humidity = models.FloatField()
    Min_Lightintensity = models.FloatField()
    Max_Lightintensity = models.FloatField()

class Condition(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField()
    Temperature = models.FloatField()
    Humidity = models.FloatField()
    Lightintensity = models.FloatField()