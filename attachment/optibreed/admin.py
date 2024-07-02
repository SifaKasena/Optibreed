from django.contrib import admin
from .models import Room, Condition

# Register your models here.
admin.site.register([Room, Condition])
