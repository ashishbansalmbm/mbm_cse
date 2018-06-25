from django.shortcuts import render
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import View
from .models import User
from django.urls import reverse_lazy
from django.contrib.auth import authenticate, login


# Create your views here.
class UserList(generic.ListView):
    template_name = 'user/user_list.html'
    context_object_name = 'user_list'

    def get_queryset(self):
        return User.objects.all()


class UserProfile(generic.DetailView):
    model = User
    template_name = 'user/user_details.html'
    context_object_name = 'user_list'


class UserCreate(CreateView):
    model = User
    fields = ['user_name', 'password', 'name', 'date_of_birth', 'gender',
              'address', 'city', 'state', 'contact', 'email', 'photo', 'category', 'blood_group', 'type']


class UserUpdate(UpdateView):
    model = User
    fields = ['user_name', 'password', 'name', 'date_of_birth', 'gender',
              'address', 'city', 'state', 'contact', 'email', 'photo', 'category', 'blood_group', 'type']


class UserDelete(DeleteView):
    model = User
    success_url = reverse_lazy('user:user_list')



