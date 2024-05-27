from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login,logout
from .forms import RegistrationForm
from .models import User
from.models import Room
from django.contrib.auth.decorators import login_required

# Create your views here.
#landing page
def index(request):
    return render(request, 'index.html')


class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = RegistrationForm
    success_url = '/home/'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

@login_required
def home(request):
    username = request.user.username
    rooms = Room.objects.filter(User=request.user)  # Fetch all rooms from the database associated with logged in user
    return render(request, 'home.html', {'username': username, 'rooms': rooms})


#add room

from .forms import RoomForm

@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)  # Create a Room instance but don't save to the database yet
            room.User = request.user  # Set the User field to the logged-in user
            room.save()  # Save the Room instance to the database
            return redirect('optibreed:home')  # Redirect to a success page or another relevant page
    else:
        form = RoomForm()
    return render(request, 'add_room.html', {'form': form})







#collect data from sensor
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Condition, Room  # Ensure you import your models

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')  # Ensure the data contains a room_id
            timestamp = data.get('timestamp')
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            light_intensity = data.get('light_intensity')

            # Find the room instance (Assuming Room model exists)
            room = Room.objects.get(id=room_id)
            
            # Create and save the Condition instance
            Condition.objects.create(
                Room=room,
                Timestamp=timestamp,
                Temperature=temperature,
                Humidity=humidity,
                Lightintensity=light_intensity
            )
            
            return JsonResponse({"status": "success"}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "failure", "reason": "Invalid JSON"}, status=400)
        except Room.DoesNotExist:
            return JsonResponse({"status": "failure", "reason": "Room not found"}, status=404)
    return JsonResponse({"status": "failure", "reason": "Invalid request method"}, status=405)




# viauslize historical data

def room_conditions(request, room_id):
    # Fetch the room and its conditions
    room = Room.objects.get(id=room_id, User=request.user)
    conditions = Condition.objects.filter(Room=room).order_by('-Timestamp')[:50]  # Limit to first 50 records

    labels = [condition.Timestamp.strftime('%Y-%m-%d %H:%M:%S') for condition in conditions]
    temperatures = [condition.Temperature for condition in conditions]
    humidities = [condition.Humidity for condition in conditions]
    light_intensities = [condition.Lightintensity for condition in conditions]

    context = {
        'room': room,
        'conditions': conditions,
        'labels': json.dumps(labels),  # Convert to JSON for JavaScript
        'temperatures': json.dumps(temperatures),
        'humidities': json.dumps(humidities),
        'light_intensities': json.dumps(light_intensities)
    }

    return render(request, 'room.html', context)


# def detail(request, room_id):
    
#     room_conditions(request,room_id)
#     return render(request, 'room.html', {'room': room})


#edit room information

def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('optibreed:rooms', room_id=room_id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'edit_room.html', {'form': form})




#displaying updated condition

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Condition
from .serializers import ConditionSerializer

class LatestConditionView(APIView):
    def get(self, request, room_id, format=None):
        try:
            latest_condition = Condition.objects.filter(Room__id=room_id).latest('Timestamp')
            serializer = ConditionSerializer(latest_condition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Condition.DoesNotExist:
            return Response({"error": "No condition records found for this room."}, status=status.HTTP_404_NOT_FOUND)
