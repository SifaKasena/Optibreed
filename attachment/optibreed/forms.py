# forms.py (in your app)
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Room
from django import forms


# class RegistrationForm(UserCreationForm):
#     """
#     A form used for user registration.

#     Inherits from UserCreationForm, which is a built-in form provided by Django
#     for creating new user accounts.

#     Attributes:
#         model (User): The user model to be used for registration.
#         fields (list): The fields to be included in the registration form.

#     """
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1', 'password2']

#     def __init__(self, *args, **kwargs):
#         super(RegistrationForm, self).__init__(*args, **kwargs)
#         self.fields['username'].widget = forms.TextInput(attrs={'placeholder': 'Username'})
#         self.fields['email'].widget = forms.EmailInput(attrs={'placeholder': 'Email'})
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Password'})
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})


# form for adding room
class RoomForm(forms.ModelForm):
    """
    A form for creating or updating a Room object.

    This form is used to collect and validate data for the Room model.
    It includes fields for the material name, minimum and maximum temperature,
    minimum and maximum humidity, and minimum and maximum light intensity.

    Attributes:
        model (Room): The Room model that this form is associated with.
        exclude (list): A list of fields to exclude from the form.
        fields (list): A list of fields to include in the form.

    """
    class Meta:
        model = Room
        exclude = ['User']
        fields = [
            'Material_name', 'Min_Temperature', 'Max_Temperature',
            'Min_Humidity', 'Max_Humidity', 'Min_Lightintensity', 'Max_Lightintensity'
        ]


# class ReportForm(forms.Form):
#     """
#     A form for generating reports.

#     This form allows users to select the type of report they want to generate,
#     specify the number of records to include, and provide a date range for the report.

#     Attributes:
#         report_type (ChoiceField): A choice field for selecting the type of report.
#         number_of_records (IntegerField): An optional field for specifying the number of records to include.
#         start_date (DateTimeField): An optional field for specifying the start date of the report.
#         end_date (DateTimeField): An optional field for specifying the end date of the report.
#     """

#     RECORD_CHOICES = [
#         ('recent', 'Most Recent Records'),
#         ('date_range', 'Date Range')
#     ]
#     report_type = forms.ChoiceField(choices=RECORD_CHOICES, required=True)
#     number_of_records = forms.IntegerField(required=False, min_value=1)
#     start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))
#     end_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}))



class ReportForm(forms.Form):
    def __init__(self, user, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['room_id'] = forms.ModelChoiceField(queryset=Room.objects.filter(User=user), label='Select Room')
    
    report_type = forms.ChoiceField(choices=[('recent', 'Recent'), ('date_range', 'Date Range')], label='Report Type')
    number_of_records = forms.ChoiceField(choices=[(10, '10'), (25, '25'), (50, '50'), (75, '75'), (100, '100'), ('all', 'All')], label='Number of Records')
    start_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='Start Date')
    end_date = forms.DateTimeField(required=False, widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}), label='End Date')
    order = forms.ChoiceField(choices=[('asc', 'Ascending'), ('desc', 'Descending')], label='Order')
    file_type = forms.ChoiceField(choices=[('pdf', 'PDF'), ('word', 'Word Document')], label='File Type')
