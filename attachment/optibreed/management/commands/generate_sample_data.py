#optibreed/management/commands/generate_sample_data.py
from django.core.management.base import BaseCommand
from optibreed.models import Condition, Room
import random
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Generate sample data for Condition model'

    def handle(self, *args, **kwargs):
    
        room = Room.objects.get(id=1)  # Replace with specific room if necessary

        if not room:
            self.stdout.write(self.style.ERROR('No Room instances found. Please create a Room instance first.'))
            return

        # Generate sample data
        for i in range(100):  # Generate 100 sample entries
            timestamp = datetime.now() - timedelta(days=i)
            temperature = random.uniform(18.0, 30.0)
            humidity = random.uniform(30.0, 70.0)
            light_intensity = random.uniform(100.0, 1000.0)

            Condition.objects.create(
                Room=room,
                Timestamp=timestamp,
                Temperature=temperature,
                Humidity=humidity,
                Lightintensity=light_intensity
            )

        self.stdout.write(self.style.SUCCESS('Successfully generated sample data'))
