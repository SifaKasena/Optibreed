from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.contrib.auth import login
from .forms import RegistrationForm

# Create your views here.
def index(request):
    return HttpResponse("Hello, world. You're at the index page.")

class SignupView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = RegistrationForm
    success_url = '/home/'
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return HttpResponseRedirect(self.success_url)

def home(request):
    return HttpResponse("Hello, world. You're at the home page.")
