from django.db import models
from django.contrib.auth.models import User
from enumerations.enum import MessageType
from datetime import datetime

# Create your models here.


class Group(models.Model):
    created_by = models.ForeignKey(User, on_delete=None)
    # Creation Date Time
    created_on = models.DateTimeField(auto_now=datetime)
    group_name = models.CharField(max_length=20, unique=True)
    # Contains IDs of receivers
    group_list = models.TextField()
    group_id = models.CharField(max_length=20)

    class Meta:
        permissions = (
                       ('can_create_group', 'can create message groups'),
                       )

    def __str__(self):
        return self.group_name


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=None, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=None, related_name='receiver', null=True)
    type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in MessageType], default=MessageType.M)
    date = models.DateTimeField(auto_now_add=datetime)
    read = models.BooleanField(default=False)
    message = models.CharField(max_length=250)
    attachment = models.FileField(upload_to='message_attachments', blank=True)
    receiver_group = models.ForeignKey(Group, on_delete=None, null=True)

    class Meta:
        permissions = (('can_send_message', 'can send messages'),
                       ('can_receive_message', 'can receive messages'),
                       ('can_read_message', 'can read messages'),
                       )


class Block(models.Model):
    sender = models.ForeignKey(User, on_delete=None, related_name='block_sender')
    receiver = models.ForeignKey(User, on_delete=None, related_name='block_receiver')

    class Meta:
        permissions = (
                       ('can_block_users', 'can block users'),
                       ('can_unblock_users', 'can unblock users'),
                       )


class Notification(models.Model):
    created_on = models.DateTimeField(auto_now=datetime)
    created_by = models.CharField(max_length=100)
    information = models.TextField()
    attachment = models.FileField(blank=True)
    duration = models.IntegerField(default=31, help_text="Default 31 days,Enter to Overwrite.(No of Days)")

    class Meta:
        permissions = (
                       ('can_send_notification', 'can send notification on homepage'),
                       )

