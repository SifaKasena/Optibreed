from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Room(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Material_name = models.CharField(max_length=50)
    OPT_Temperature = models.FloatField()
    OPT_Humidity = models.FloatField()
    OPT_Lightintensity = models.FloatField()

class Condition(models.Model):
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField()
    Temperature = models.FloatField()
    Humidity = models.FloatField()
    Lightintensity = models.FloatField()