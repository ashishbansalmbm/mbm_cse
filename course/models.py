from django.db import models
from program.models import Program
from user.models import User
from department.models import Department
#from forum.models import Forum
from enumerations.enum import CourseType, Semester


class Course(models.Model):
    department = models.ForeignKey(Department, on_delete=None)
    semester = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in Semester)
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50)
    course_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in CourseType)
    max_marks = models.IntegerField()
    credits = models.PositiveSmallIntegerField()
    objective = models.TextField()
    syllabus = models.TextField()
    text_books = models.TextField()
    ref_material = models.TextField()
    prerequisite = models.TextField()
    duration = models.DurationField()
    hours = models.DurationField()
    updated_on = models.DateField()
    # forum = models.ForeignKey(Forum, on_delete=None) ##
 
 
class CourseProgram(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    program = models.ForeignKey(Program, on_delete=None)
 
 
class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=None)
    year = models.PositiveSmallIntegerField()


class CourseOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    text = models.TextField()
    strong_po = models.CharField(max_length=50)
    weak_po = models.CharField(max_length=50)


class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    year = models.DateField()
    active = models.BooleanField(default=False)


class CourseAvailable(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    faculty = models.ForeignKey(User, on_delete=None)
    year = models.DateField()
    active = models.BooleanField()
