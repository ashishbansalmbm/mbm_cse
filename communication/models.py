from django.db import models
from django.contrib.auth.models import User
from enumerations.enum import MessageType
from datetime import datetime

# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=None, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=None, related_name='receiver')
    type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in MessageType], default=MessageType.M)
    date = models.DateTimeField(auto_now_add=datetime)
    read = models.BooleanField(default=False)
    message = models.CharField(max_length=250)
    attachment = models.FileField(upload_to='message_attachments', blank=True)


class Block(models.Model):
    sender = models.ForeignKey(User, on_delete=None, related_name='block_sender')
    receiver = models.ForeignKey(User, on_delete=None, related_name='block_receiver')