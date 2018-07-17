from django import forms
from .models import Message
from user.models import Profile
from django.contrib.auth.models import User
import django_filters


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['receiver', 'sender', 'date', 'read']