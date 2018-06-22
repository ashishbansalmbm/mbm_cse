from django.db import models
from program.models import Program
from user.models import User
from enum import Enum
from department.models import Department
#from forum.models import Forum
from user.models import User
from enumerations.enum import FeedbackQuestionType, Semester


class Course(models.Model):
    semester = [(tag, tag.value) for tag in Semester ]
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50)
    max_marks = models.IntegerField()
    credits = models.PositiveSmallIntegerField()
    objective = models.TextField()
    syllabus = models.TextField()
    text_books = models.TextField()
    ref_material = models.TextField()
    prerequisite = models.TextField()
    course_type = models.CharField(max_length=50)
    duration = models.DurationField()
    hours = models.DurationField()
    updated_on = models.DateField()
    program = models.ForeignKey(Program, on_delete=None)
    # forum = models.ForeignKey(Forum, on_delete=None) ##


class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=None)
    year = models.DateField()


class CourseOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    text = models.TextField()


class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    year = models.DateField()
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=None)

class CourseAvailable(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    faculty = models.ForeignKey(User, on_delete=None)
    year = models.DateField()
    active = models.BooleanField()
