from django.db import models
from user.models import User
from course.models import Course
from program.models import Program
from department.models import Department
# Create your Student models here.


class Student(models.Model):
    semester = models.ForeignKey(Course, on_delete=None)
    program = models.ForeignKey(Program, on_delete=None)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    date_of_admission = models.DateField()
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    area_of_interest = models.TextField()
    carrier_objective = models.TextField()
