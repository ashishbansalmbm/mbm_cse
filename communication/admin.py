from django.contrib import admin
from .models import Message, Block, Group,Notification
# Register your models here.
admin.site.register(Message)
admin.site.register(Block)
admin.site.register(Group)
admin.site.register(Notification)