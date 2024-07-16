import base64
import json
import tempfile
from io import BytesIO
import matplotlib
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import RegistrationForm, ReportForm, RoomForm
from .models import Condition, Room, Notification
from .serializers import ConditionSerializer
import matplotlib.pyplot as plt
from django.db.models import Min, Max
from datetime import datetime, timedelta, date


# Create your views here.
def index(request):

    if request.user.is_authenticated:
        return redirect('optibreed:dashboard')

    return render(request, 'public/index.html')



class SignupView(generic.CreateView):

    template_name = "registration/signup.html"
    form_class = RegistrationForm
    success_url = '/dashboard/'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)


@login_required
def dashboard(request):
    rooms = Room.objects.all()
    Room_id = rooms.values_list('id', flat=True)  # Fetch all Room IDs
    
    time_frame = request.GET.get('time_frame', 'today')
    today = date.today()
    
    if time_frame == 'today':
        conditions = Condition.objects.filter(Room_id__in=Room_id, Timestamp__date=today).order_by('-Timestamp')
    elif time_frame == 'this_week':
        start_of_week = today - timedelta(days=today.weekday())
        conditions = Condition.objects.filter(Room_id__in=Room_id, Timestamp__date__gte=start_of_week).order_by('-Timestamp')
    elif time_frame == 'this_month':
        start_of_month = today.replace(day=1)
        conditions = Condition.objects.filter(Room_id__in=Room_id, Timestamp__date__gte=start_of_month).order_by('-Timestamp')
    else:
        conditions = Condition.objects.filter(Room_id__in=Room_id).order_by('-Timestamp')

    min_temperature = conditions.aggregate(Min('Temperature'))['Temperature__min']
    max_temperature = conditions.aggregate(Max('Temperature'))['Temperature__max']
    min_humidity = conditions.aggregate(Min('Humidity'))['Humidity__min']
    max_humidity = conditions.aggregate(Max('Humidity'))['Humidity__max']
    min_light_intensity = conditions.aggregate(Min('Lightintensity'))['Lightintensity__min']
    max_light_intensity = conditions.aggregate(Max('Lightintensity'))['Lightintensity__max']

    temperatures = [condition.Temperature for condition in conditions]
    humidities = [condition.Humidity for condition in conditions]
    light_intensities = [condition.Lightintensity for condition in conditions]
    timestamps = [condition.Timestamp.strftime('%Y-%m-%dT%H:%M:%S.%fZ') for condition in conditions]

    context = {
        'rooms': rooms,
        'conditions': conditions[:1],  # Only pass the latest condition
        'min_temperature': min_temperature,
        'max_temperature': max_temperature,
        'min_humidity': min_humidity,
        'max_humidity': max_humidity,
        'min_light_intensity': min_light_intensity,
        'max_light_intensity': max_light_intensity,
        'temperatures': temperatures,
        'humidities': humidities,
        'light_intensities': light_intensities,
        'timestamps': timestamps,
        'time_frame': time_frame,
    }
    return render(request, 'core/dashboard/dashboard.html', context)



@login_required
def rooms(request):
    rooms = Room.objects.filter(User=request.user)
    return render(request, 'core/room/rooms.html', {'rooms': rooms})


@login_required
def add_room(request):
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            room = form.save(commit=False)
            room.User = request.user
            room.save()
            return redirect('optibreed:rooms')
    else:
        form = RoomForm()

    return render(request, 'core/rooms/add_room.html', {'form': form})


@login_required
def edit_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('optibreed:rooms', room_id=room_id)
    else:
        form = RoomForm(instance=room)
    return render(request, 'core/room/edit_room.html', {'form': form})

@csrf_exempt
def receive_data(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            room_id = data.get('room_id')
            timestamp = data.get('timestamp')
            temperature = data.get('temperature')
            humidity = data.get('humidity')
            light_intensity = data.get('light_intensity')

            room = Room.objects.get(id=room_id)
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

@login_required
def room_conditions(request, room_id):
    room = Room.objects.get(id=room_id, User=request.user)
    conditions = Condition.objects.filter(Room=room).order_by('-Timestamp')[:50]  # Limit to first 50 records
    conditions_reverse = conditions[::-1]

    labels = [condition.Timestamp.strftime('%Y-%m-%d %H:%M:%S') for condition in conditions_reverse]
    temperatures = [condition.Temperature for condition in conditions_reverse]
    humidities = [condition.Humidity for condition in conditions_reverse]
    light_intensities = [condition.Lightintensity for condition in conditions_reverse]

    context = {
        'room': room,
        'conditions': conditions,
        'labels': json.dumps(labels),
        'temperatures': json.dumps(temperatures),
        'humidities': json.dumps(humidities),
        'light_intensities': json.dumps(light_intensities)
    }

    return render(request, 'core/room/room_details.html', context)


# Notifications list view
@login_required
def notifications_list(request):
    status = request.GET.get('status')
    date = request.GET.get('date')

    notifications = Notification.objects.filter(User=request.user)

    if status:
        notifications = notifications.filter(status=status)
    if date:
        notifications = notifications.filter(timestamp__date=date)

    context = {
        'notifications': notifications
    }

    return render(request, 'core/notifications/list.html', context)


# Notification details view
@login_required
def notification_details(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id, User=request.user)

    context = {
        'notification': notification
    }

    return render(request, 'notifications/details.html', context)

# Displaying updated condition
class LatestConditionView(APIView):

    def get(self, request, room_id, format=None):
        """Retrieves the latest condition record for the specified room."""
        try:
            latest_condition = Condition.objects.filter(Room__id=room_id).latest('Timestamp')
            serializer = ConditionSerializer(latest_condition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Condition.DoesNotExist:
            return Response({"error": "No condition records found for this room."}, status=status.HTTP_404_NOT_FOUND)


matplotlib.use('Agg')  # Use the Anti-Grain Geometry backend for non-interactive plotting


def generate_chart(labels, data, title, ylabel):

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

def generate_report(request):
    form = ReportForm(request.GET or None)
    form.user = request.user  # Pass the user to the form

    conditions = Condition.objects.none()
    report_data = {}
    image_temp = None
    image_hum = None
    image_light = None

    if form.is_valid():
        room = form.cleaned_data['room_id']
        report_type = form.cleaned_data['report_type']
        number_of_records = form.cleaned_data['number_of_records']
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
        order = form.cleaned_data['order']
        file_type = form.cleaned_data['file_type']

        conditions = Condition.objects.filter(Room=room)

        if report_type == 'recent':
            if number_of_records != 'all':
                conditions = conditions.order_by('-Timestamp')[:int(number_of_records)]
        elif report_type == 'date_range':
            conditions = conditions.filter(Timestamp__range=(start_date, end_date)).order_by(order)

        avg_temperature = conditions.aggregate(Avg('Temperature'))['Temperature__avg']
        avg_humidity = conditions.aggregate(Avg('Humidity'))['Humidity__avg']
        avg_lightintensity = conditions.aggregate(Avg('Lightintensity'))['Lightintensity__avg']

        labels = [condition.Timestamp.strftime('%Y-%m-%d %H:%M:%S') for condition in conditions]
        temperatures = [condition.Temperature for condition in conditions]
        humidities = [condition.Humidity for condition in conditions]
        lightintensities = [condition.Lightintensity for condition in conditions]

        image_temp = generate_chart(labels, temperatures, 'Temperature', 'Temperature (°C)')
        image_hum = generate_chart(labels, humidities, 'Humidity', 'Humidity (%)')
        image_light = generate_chart(labels, lightintensities, 'Light Intensity', 'Light Intensity (lux)')

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

        # Add more conditions for other file types if needed

    context = {
        'form': form,
        'conditions': conditions,
        'report_data': report_data,
        'image_temp': image_temp,
        'image_hum': image_hum,
        'image_light': image_light,
    }

    return render(request, 'core/reports/reports.html', context)