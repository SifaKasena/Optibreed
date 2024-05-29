# forms.py (in your app)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room
from django import forms

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']



#form for adding room
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        exclude = ['User']
        fields = [
            'Material_name', 'Min_Temperature', 'Max_Temperature',
            'Min_Humidity', 'Max_Humidity', 'Min_Lightintensity', 'Max_Lightintensity'
        ]

class ReportForm(forms.Form):
    RECORD_CHOICES = [
        ('recent', 'Most Recent Records'),
        ('date_range', 'Date Range')
    ]
    report_type = forms.ChoiceField(choices=RECORD_CHOICES, required=True)
    number_of_records = forms.IntegerField(required=False, min_value=1)
    start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
    end_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))