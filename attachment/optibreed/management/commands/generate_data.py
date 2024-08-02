import requests
import time
from datetime import datetime
from random import uniform, choice
from django.core.management.base import BaseCommand
from optibreed.models import Room

class Command(BaseCommand):
    help = 'Generate random data for Condition model'
    url = 'http://localhost:8000/endpoint/'

    def handle(self, *args, **kwargs):
        while True:
            rooms = Room.objects.all()
            for room in rooms:
                data = {
                    'room_id': room.id,
                    'timestamp': datetime.now().isoformat(),
                    'temperature': uniform(room.Min_Temperature - 5, room.Max_Temperature + 5),
                    'humidity': uniform(room.Min_Humidity - 5, room.Max_Humidity + 5),
                    'voltage': uniform(room.Min_Voltage - 5, room.Max_Voltage + 5),
                    'door_condition': choice(['Open', 'Closed'])
                }

                try:
                    response = requests.post(self.url, json=data)
                    if response.status_code != 200:
                        print(f"Error: {response.text}")
                except Exception as e:
                    print(f"Request failed: {e}")

            time.sleep(30)
