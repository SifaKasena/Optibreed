from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login
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

@login_required
def detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'room.html', {'room': room})