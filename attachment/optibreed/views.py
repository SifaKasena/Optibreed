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



#generating reports

# views.py


# def generate_report(request, room_id):
    # room = Room.objects.get(id=room_id, User=request.user)
    # form = ReportForm(request.GET or None)
    # conditions = []
    # report_data = {}
    # if form.is_valid():
    #     report_type = form.cleaned_data['report_type']
    #     if report_type == 'recent':
    #         number_of_records = form.cleaned_data['number_of_records']
    #         conditions = Condition.objects.filter(Room=room).order_by('-Timestamp')[:number_of_records]
    #     elif report_type == 'date_range':
    #         start_date = form.cleaned_data['start_date']
    #         end_date = form.cleaned_data['end_date']
    #         conditions = Condition.objects.filter(Room=room, Timestamp__range=(start_date, end_date)).order_by('Timestamp')
        
    #     # Calculate average statistics
    #     avg_temperature = conditions.aggregate(Avg('Temperature'))['Temperature__avg']
    #     avg_humidity = conditions.aggregate(Avg('Humidity'))['Humidity__avg']
    #     avg_lightintensity = conditions.aggregate(Avg('Lightintensity'))['Lightintensity__avg']
        
    #     report_data = {
    #         'avg_temperature': avg_temperature,
    #         'avg_humidity': avg_humidity,
    #         'avg_lightintensity': avg_lightintensity
    #     }

    #     # Generate plots
    #     labels = [condition.Timestamp.strftime('%Y-%m-%d %H:%M:%S') for condition in conditions]
    #     temperatures = [condition.Temperature for condition in conditions]
    #     humidities = [condition.Humidity for condition in conditions]
    #     lightintensities = [condition.Lightintensity for condition in conditions]

    #     # Temperature plot
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(labels, temperatures, label='Temperature', color='red')
    #     plt.xlabel('Timestamp')
    #     plt.ylabel('Temperature (°C)')
    #     plt.title('Temperature Over Time')
    #     plt.xticks(rotation=45)
    #     plt.tight_layout()
        
    #     buf = io.BytesIO()
    #     plt.savefig(buf, format='png')
    #     buf.seek(0)
    #     image_base64_temp = base64.b64encode(buf.read()).decode('utf-8')
    #     plt.close()
        
    #     report_data['image_base64_temp'] = image_base64_temp

    #     # Humidity plot
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(labels, humidities, label='Humidity', color='blue')
    #     plt.xlabel('Timestamp')
    #     plt.ylabel('Humidity (%)')
    #     plt.title('Humidity Over Time')
    #     plt.xticks(rotation=45)
    #     plt.tight_layout()
        
    #     buf = io.BytesIO()
    #     plt.savefig(buf, format='png')
    #     buf.seek(0)
    #     image_base64_hum = base64.b64encode(buf.read()).decode('utf-8')
    #     plt.close()
        
    #     report_data['image_base64_hum'] = image_base64_hum

    #     # Light Intensity plot
    #     plt.figure(figsize=(10, 6))
    #     plt.plot(labels, lightintensities, label='Light Intensity', color='green')
    #     plt.xlabel('Timestamp')
    #     plt.ylabel('Light Intensity (lux)')
    #     plt.title('Light Intensity Over Time')
    #     plt.xticks(rotation=45)
    #     plt.tight_layout()
        
    #     buf = io.BytesIO()
    #     plt.savefig(buf, format='png')
    #     buf.seek(0)
    #     image_base64_light = base64.b64encode(buf.read()).decode('utf-8')
    #     plt.close()
        
    #     report_data['image_base64_light'] = image_base64_light

    # context = {
    #     'room': room,
    #     'user': request.user,
    #     'form': form,
    #     'conditions': conditions,
    #     'report_data': report_data
    # }
    # return render(request, 'report.html', context)

from django.shortcuts import render
from .models import Condition, Room
from .forms import ReportForm
import matplotlib
matplotlib.use('Agg')  # Use the Anti-Grain Geometry backend for non-interactive plotting
import matplotlib.pyplot as plt
import io
import base64
from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.db.models import Avg
from .models import Condition, Room
from .forms import ReportForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import base64
import tempfile

def generate_report(request, room_id):
    room = get_object_or_404(Room, id=room_id, User=request.user)
    form = ReportForm(request.GET or None)
    conditions = Condition.objects.filter(Room=room).order_by('-Timestamp')

    if form.is_valid():
        report_type = form.cleaned_data['report_type']
        number_of_records = form.cleaned_data['number_of_records']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']

        if report_type == 'recent':
            conditions = conditions[:number_of_records]
        elif report_type == 'date_range':
            conditions = conditions.filter(Timestamp__range=(start_date, end_date))

    avg_temperature = conditions.aggregate(Avg('Temperature'))['Temperature__avg']
    avg_humidity = conditions.aggregate(Avg('Humidity'))['Humidity__avg']
    avg_lightintensity = conditions.aggregate(Avg('Lightintensity'))['Lightintensity__avg']

    # Generate plots
    labels = [condition.Timestamp.strftime('%Y-%m-%d %H:%M:%S') for condition in conditions]
    temperatures = [condition.Temperature for condition in conditions]
    humidities = [condition.Humidity for condition in conditions]
    lightintensities = [condition.Lightintensity for condition in conditions]

    def generate_chart(data, title, ylabel):
        plt.figure(figsize=(10, 6))
        plt.plot(labels, data, label=title)
        plt.xlabel('Timestamp')
        plt.ylabel(ylabel)
        plt.title(f'{title} Over Time')
        plt.xticks(rotation=45)
        buf = BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        image_data = buf.read()
        plt.close()
        return image_data

    image_temp = generate_chart(temperatures, 'Temperature', 'Temperature (°C)')
    image_hum = generate_chart(humidities, 'Humidity', 'Humidity (%)')
    image_light = generate_chart(lightintensities, 'Light Intensity', 'Light Intensity (lux)')

    report_data = {
        'avg_temperature': avg_temperature,
        'avg_humidity': avg_humidity,
        'avg_lightintensity': avg_lightintensity,
    }

    if 'download_pdf' in request.GET:
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="report_{room.Material_name}.pdf"'

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter

        p.drawString(100, height - 100, f"Condition Report for Room: {room.Material_name}")
        p.drawString(100, height - 120, f"User: {request.user.username}")

        p.drawString(100, height - 160, f"Average Temperature: {avg_temperature:.2f}°C")
        p.drawString(100, height - 180, f"Average Humidity: {avg_humidity:.2f}%")
        p.drawString(100, height - 200, f"Average Light Intensity: {avg_lightintensity:.2f} lux")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_temp)
            p.drawImage(temp_file.name, 100, height - 400, width=400, height=150)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_hum)
            p.drawImage(temp_file.name, 100, height - 600, width=400, height=150)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp_file:
            temp_file.write(image_light)
            p.drawImage(temp_file.name, 100, height - 800, width=400, height=150)

        p.showPage()
        p.save()

        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response

    context = {
        'room': room,
        'user': request.user,
        'conditions': conditions,
        'form': form,
        'report_data': report_data,
        'image_base64_temp': base64.b64encode(image_temp).decode('utf-8'),
        'image_base64_hum': base64.b64encode(image_hum).decode('utf-8'),
        'image_base64_light': base64.b64encode(image_light).decode('utf-8')
    }

    return render(request, 'report.html', context)
