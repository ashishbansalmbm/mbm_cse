from django.db import models
from enumerations.enum import QuestionType, AssessmentType
from user.models import User
from course.models import Course, CourseOutcome
from faculty.models import Faculty


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    type = [(tag, tag.value) for tag in AssessmentType]
    start_date = models.DateField()
    duration = models.DurationField()
    faculty_id = models.ForeignKey(Faculty, on_delete=None)
    year = models.PositiveSmallIntegerField()


class AssessmentQuestion(models.Model):
    question_type = [(tag, tag.value) for tag in QuestionType]
    assessment = models.ForeignKey(Assessment, on_delete=None)
    text = models.TextField()
    max_marks = models.PositiveSmallIntegerField()
    question_order = models.PositiveSmallIntegerField()
    marking_scheme = models.TextField()
    outcome = models.ForeignKey(CourseOutcome , on_delete=None)


class AssessmentResult(models.Model):
    question = models.ForeignKey(AssessmentQuestion, on_delete=None)
    student = models.ForeignKey(User, on_delete=None)
    obtained_marks = models.PositiveSmallIntegerField()
    remarks = models.TextField()
