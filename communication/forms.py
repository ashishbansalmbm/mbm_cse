
from django import forms
from .models import Message, Group,Notification
from user.models import Profile
from django.contrib.auth.models import User


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        exclude = ['receiver', 'sender', 'date', 'read', 'receiver_group']


class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['group_name']
class NotificationForm(forms.ModelForm):
    class Meta:
        model=Notification
        fields=['information','duration','attachment']
