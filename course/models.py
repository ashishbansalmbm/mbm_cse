from django.db import models
from program.models import Program
from user.models import User
from enum import Enum
from department.models import Department
from forum.models import Forum
from user.models import User


class FeedbackQuestionType(Enum):
    TF = 'True/False'
    MCQ = 'Multiple Choice'
    R = 'Rating'


class Semester(Enum):
    SEM_1 = '1st Semester'
    SEM_2 = '2nd Semester'
    SEM_3 = '3rd Semester'
    SEM_4 = '4th Semester'
    SEM_5 = '5th Semester'
    SEM_6 = '6th Semester'
    SEM_7 = '7th Semester'
    SEM_8 = '8th Semester'


class Course(models.Model):
    department = models.ForeignKey(Department,on_delete=None)
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
    type = models.CharField(max_length=50)
    duration = models.DurationField()
    hours = models.DurationField()
    updated_on = models.DateField()
    program = models.ForeignKey(Program, on_delete=None)
    forum = models.ForeignKey(Forum, on_delete=None) ##


class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=None)
    year = models.PositiveSmallIntegerField() # should use date ,default on creation


class CourseOutcomes(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    text = models.TextField()


class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    year = models.DateField()
    active = models.BooleanField(default=False)


class FeedbackQuestion(models.Model):
    feedback = models.ForeignKey(CourseFeedback, on_delete=None)
    type = models.CharField([(tag, tag.value) for tag in FeedbackQuestionType])
    options = models.PositiveSmallIntegerField()
    quesText = models.TextField()
    order = models.PositiveSmallIntegerField()


class FeedbackAnswer(models.Model):
    question = models.ForeignKey(FeedbackQuestion)
    user = models.ForeignKey(User, on_delete=None)
    answer = models.TextField()


class CourseAvailable(models.Model):
    course = models.ForeignKey(Course,on_delete=None)
    faculty = models.ForeignKey(User, on_delete=None)
    year = models.DateField()
    active = models.BooleanField()