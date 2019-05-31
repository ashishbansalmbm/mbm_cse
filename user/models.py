from email.policy import default

from django.db import models
from enumerations.enum import UserType, BloodGroup, Gender, Category
from django.urls import reverse
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from datetime import date

# Create your models here.
# User Table


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=date.today)
    gender = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in Gender], default='')
    address = models.CharField(max_length=200, default='')
    city = models.CharField(max_length=10, default='')
    state = models.CharField(max_length=10, default='')
    contact = models.CharField(max_length=15, default='+919876543210')
    photo = models.ImageField(upload_to='profile_photo', help_text='Your Photo name should be same as your name' , blank=True)
    category = models.CharField(max_length=5, choices=[(tag.name, tag.value) for tag in Category],
                                default='')
    blood_group = models.CharField(max_length=5, choices=[(tag.name, tag.value) for tag in BloodGroup],
                                   default='')
    type = models.CharField(max_length=3, choices=[(tag.name, tag.value) for tag in UserType], default='')
    verified = models.BooleanField(default=False)

    class Meta:
        permissions = (
                        ('can_view_profile', 'can view self profile'),
                        ('can_update_profile', 'can update profile')
        )

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

    def get_absolute_url(self):
        return reverse('user:home')


# Automatically Called Whenever an user instance is created
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        user_profile = Profile.objects.create(user=user)
        user_profile.save()


post_save.connect(create_profile, sender=User)


class NewsLetterSubscription(models.Model):
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.email










