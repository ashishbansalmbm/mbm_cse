from django import forms
from student.models import Student


class StudentProfile(forms.ModelForm):
    class Meta:
        model = Student
        exclude = ['user', 'date_of_admission']


class StudentProfileSubmit(forms.ModelForm):

    class Meta:
        model = Student
        fields = ['area_of_interest', 'carrier_objective']
