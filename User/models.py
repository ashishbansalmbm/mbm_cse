from django.db import models

# Create your models here.
# User Table

class User(models.Model):
    User_id = models.CharField(primary_key=True, unique=True, max_length=30)
    Password = models.CharField(max_length=16)
    Name = models.CharField(max_length=50)
    Date_of_birth = models.DateField()
    Sex = models.CharField(max_length=10)
    Address = models.CharField(max_length=200)
    City = models.CharField(max_length=20)
    State = models.CharField(max_length=20)
    Contact = models.IntegerField()
    Email = models.EmailField()
    Photo = models.ImageField()
    Category = models.CharField(max_length=10)
    Blood_group = models.CharField(max_length=3,null=True)

