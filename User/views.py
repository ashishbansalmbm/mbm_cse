from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import User

# Create your views here.
class UserList(generic.ListView):
    template_name = 'user/User_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()


class UserProfile(generic.DetailView):
    model = User
    template_name = 'user/User_details.html'
    context_object_name = 'user_list'


class UserCreate(CreateView):
    model = User
    fields =['User_id', 'Password', 'Name', 'Date_of_birth', 'Sex',
             'Address', 'City', 'State', 'Contact', 'Email', 'Photo', 'Category', 'Blood_group',
         ]