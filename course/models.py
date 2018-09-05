from django.contrib.auth.models import User
from django.db import models
from program.models import Program,ProgramOutcome
from user.models import Profile
import datetime
# from forum.models import Forum
from django.urls import reverse
from enumerations.enum import CourseType, Semester, CoPoLink


class Course(models.Model):
    semester = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in Semester],
                                default=Semester.SEM_1)
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50)
    course_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in CourseType],
                                   default=CourseType.MTH)
    max_marks = models.IntegerField()
    credits = models.PositiveSmallIntegerField()
    objective = models.TextField()
    syllabus = models.TextField()
    text_books = models.TextField()
    ref_material = models.TextField()
    prerequisite = models.TextField()
    duration = models.PositiveSmallIntegerField()
    hours = models.PositiveSmallIntegerField()
    updated_on = models.DateField("Date", default=datetime.date.today)
    deleted = models.BooleanField(default=False)
    # forum = models.ForeignKey(Forum, on_delete=None)

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('name', 'course_code', 'semester',),
        permissions = (
            ('can_view_course', 'can view course '),

            ('can_create_course_faculty','can add course faculty'),

             )


class CourseProgram(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    program = models.ForeignKey(Program, on_delete=None)


class CourseAvailable(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    faculty = models.ForeignKey(User, on_delete=None)
    year = models.PositiveIntegerField()
    active = models.BooleanField(default=True)


class CourseEnrollment(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=None)
    year = models.PositiveIntegerField(default='2000')

    class Meta:
        unique_together = ('student','year',),
        permissions = (
            ('can_view_mycourse_faculty', 'can view mycourse faculty'),

            ('can_view_mycourse_student', 'can view mycourse student'),


        )


class CourseOutcome(models.Model):
    course = models.ForeignKey(Course, on_delete=None,)
    text = models.TextField()




class CourseFeedback(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    year = models.PositiveIntegerField()
    active = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=None)

    def __str__(self):
        return self.id


class CoPo(models.Model):
    program_outcome = models.ForeignKey(ProgramOutcome, on_delete=None)
    course_outcome = models.ForeignKey(CourseOutcome, on_delete=None)
    level = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in CoPoLink], default=CoPoLink.N)
    user = models.ForeignKey(User, on_delete=None)
    date = models.DateField("Date", default=datetime.date.today)

    class Meta:
        unique_together = ('program_outcome', 'course_outcome'),
