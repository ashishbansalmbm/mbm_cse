from django.db import models
from django.urls import reverse
from datetime import datetime
from user.models import User
from django.conf import settings
from django.contrib.auth.models import Permission

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.user')

class Resources(models.Model):
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    type = models.CharField(max_length=20)
    date = models.DateField(default=datetime.now())
    attachment = models.FileField()


    def get_absolute_url(self):
        return reverse('resources:index_user')

    def __str__(self):
        return self.title


    class Meta:
        permissions = {
            ('can_view_resources', 'can view resources'),
        }
