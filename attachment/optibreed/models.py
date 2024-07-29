from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class Room(models.Model):
    """
    Represents a room with temperature, humidity, and light intensity constraints.

    Attributes:
        User (ForeignKey): The user associated with the room.
        Material_name (CharField): The name of the material in the room.
        Min_Temperature (FloatField): The minimum temperature allowed in the room.
        Max_Temperature (FloatField): The maximum temperature allowed in the room.
        Min_Humidity (FloatField): The minimum humidity allowed in the room.
        Max_Humidity (FloatField): The maximum humidity allowed in the room.
        Min_Lightintensity (FloatField): The minimum light intensity allowed in the room.
        Max_Lightintensity (FloatField): The maximum light intensity allowed in the room.
    """
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    Material_name = models.CharField(max_length=50)
    Min_Temperature = models.FloatField()
    Max_Temperature = models.FloatField()
    Min_Humidity = models.FloatField()
    Max_Humidity = models.FloatField()
    Min_Lightintensity = models.FloatField()
    Max_Lightintensity = models.FloatField()

    def __str__(self):
        return self.Material_name


class Sensor(models.Model):
    """
    Represents a sensor in a room.

    Attributes:
        Room (Room): The room associated with the sensor.
        Sensor_type (CharField): The type of sensor (e.g., temperature, humidity, light intensity).
        Sensor_name (CharField): The name or identifier of the sensor.
    """
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Sensor_type = models.CharField(max_length=50)
    Sensor_name = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.Sensor_name} ({self.Sensor_type}) in {self.Room}"


class Condition(models.Model):
    """
    Represents a condition measurement in a room.

    Attributes:
        Room (Room): The room associated with the condition measurement.
        Timestamp (DateTimeField): The timestamp of the measurement.
        Temperature (FloatField): The temperature value.
        Humidity (FloatField): The humidity value.
        Lightintensity (FloatField): The light intensity value.
    """
    Room = models.ForeignKey(Room, on_delete=models.CASCADE)
    Timestamp = models.DateTimeField()
    Temperature = models.FloatField()
    Humidity = models.FloatField()
    Lightintensity = models.FloatField()

class Profile(models.Model):
    """
    Represents the profile of the user

    Attributes:
        User: the user associated with the profile
        image: profile image related to user
        job_title:job title related to user
        twitter: twitter handle account
        facebook: facebook handle account
        instagram: instagram handle account
        linkedin: linkedin handle account
        about: about section for user profile
    """
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
