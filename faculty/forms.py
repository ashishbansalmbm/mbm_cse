from .models import Faculty
from django import forms

class FacultyRegistrationForm(forms.ModelForm):
    class Meta:
        model=Faculty
        exclude=['user','submit', 'date_of_leave']

class FacultyRegistrationFormSubmit(forms.ModelForm):
    class Meta:
        model=Faculty
        exclude=['department','date_of_join','submit','user' , 'date_of_leave']
