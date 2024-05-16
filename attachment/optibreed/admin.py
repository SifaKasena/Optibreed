from django.contrib import admin

# Register your models here.
from .models import Room, Condition

admin.site.register([Room, Condition])