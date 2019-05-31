from django.db import models
from user.models import User
from course.models import Course
from program.models import Program
from department.models import Department
from enumerations.enum import Semester
from user.models import Profile
# Create your Student models here.


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=None)
    semester = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in Semester],
                                default=Semester.SEM_1)
    program = models.ForeignKey(Program, on_delete=None)
    department = models.ForeignKey(Department, on_delete=None)
    date_of_admission = models.DateField(null=True)
    mother_name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    area_of_interest = models.TextField(blank=True)
    carrier_objective = models.TextField(blank=True)
    submit = models.BooleanField(default=False)

    class Meta:
        permissions = (('can_update_profile', 'can update profile'),
                       ('can_view_student_list', ' can view student list'),
                       ('faculty_can_view_student_profile', 'faculty can view student profile'),
                       )

    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name
