from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User

# Create your views here.
class UserCreate(CreateView):
    model = User
    fields =['User_id', 'Password', 'Name', 'Date_of_birth', 'Sex',
             'Address', 'City', 'State', 'Contact', 'Email', 'Photo', 'Category', 'Blood_group',
         ]