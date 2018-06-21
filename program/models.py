from django.db import models
from user.models import User
from department.models import Department
# from course.models import CourseOutcome


class Program(models.Model):
    name = models.CharField(max_length=150)
    duration = models.DurationField()
    department = models.ForeignKey(Department, on_delete=None)


class ProgramOutcome(models.Model):
    program = models.ForeignKey(Program, on_delete=None)
    text = models.TextField()
    title = models.CharField(max_length=150)


class ProgramFeedback(models.Model):
    program = models.ForeignKey(Program, on_delete=None)
    year = models.DateField()
    active = models.BooleanField(default=False)


class CoPo(models.Model):
    program_outcome = models.ForeignKey(ProgramOutcome, on_delete=None)
   # course_outcome = models.ForeignKey(CourseOutcome, on_delete=None)
    user = models.ForeignKey(User, on_delete=None)
    date = models.DateField()
