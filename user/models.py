from django.db import models
from enum import Enum


# Create your models here.
# User Table
# enum for User_type
class UserType(Enum):
    S = "Student"
    F = "Faculty"
    U = "User"
    A = "Alumni"


# enum for blood group
class BloodGroup(Enum):
    OM = "O-Minus"
    OP = "O-Positive"
    AM = "A-Minus"
    AP = "A-Positive"
    BM = "B-Minus"
    ABM = "AB-Minus"
    ABP = "AB-Positive"
    BP = "B-Positive"



class Gender(Enum):
    M = "Male"
    F = "Female"
    OT = "Other"


class Category(Enum):
    GEN = "General"
    OBC = "Other Backward Class"
    SC = "Scheduled Caste"
    ST = "Scheduled Tribe"


class User(models.Model):
    user_name = models.CharField(unique=True, max_length=30)
    password = models.CharField(max_length=256)
    name = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    gender = [(tag, tag.value) for tag in Gender]
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=10)
    state = models.CharField(max_length=10)
    contact = models.CharField(max_length=12)
    email = models.EmailField()
    photo = models.ImageField()
    category = [(tag, tag.value) for tag in Category]
    blood_group = [(tag, tag.value) for tag in BloodGroup]
    type = [(tag, tag.value) for tag in UserType]







