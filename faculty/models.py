from django.db import models
from department.models import Department
from user.models import User
from enumerations.enum import Designation
from enum import Enum


# Create your models here.

class Faculty(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    department = models.ForeignKey(Department, on_delete=None)
    date_of_join = models.DateField()
    date_of_leave = models.DateField()
    qualification = models.CharField(max_length=50)
    designation = [(tag, tag.value) for tag in Designation]
    specialization = models.CharField(max_length=50)
    description = models.TextField()
    # employ_id = models.ForeignKey(Employ, on_delete=None)