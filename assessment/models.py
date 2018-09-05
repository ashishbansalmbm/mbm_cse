from django.db import models
from enumerations.enum import QuestionType, AssessmentType
from user.models import User
from course.models import Course, CourseOutcome
from faculty.models import Faculty
from datetime import date
from student.models import Student
from program.models import Program, ProgramOutcome
from django.contrib.auth.models import Permission
from django.urls import reverse


class Assessment(models.Model):
    course = models.ForeignKey(Course, on_delete=None)
    assessment_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in AssessmentType], default='')
    start_date = models.DateField(default=date.today)
    duration = models.DurationField()
    faculty = models.ForeignKey(Faculty, on_delete=None)
    year = models.PositiveSmallIntegerField()
    assessment_completed = models.BooleanField(default=False)
    result_completed = models.BooleanField(default=False)

    def get_absolute_url(self):
        return reverse('assessment:index')
    class Meta:
        permissions = {
            ('can_view_assessment', 'can view assessment'),
        }





class AssessmentQuestion(models.Model):
    question_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in QuestionType], default='')
    assessment = models.ForeignKey(Assessment, on_delete=None)
    text = models.TextField()
    max_marks = models.PositiveSmallIntegerField()
    question_order = models.PositiveSmallIntegerField()
    marking_scheme = models.TextField()
    outcome = models.ManyToManyField(CourseOutcome)

    def get_absolute_url(self):
        return reverse('assessment:detail', args=(self.assessment.id,))

class AssessmentResult(models.Model):
    question = models.ForeignKey(AssessmentQuestion, on_delete=None)
    student = models.ForeignKey(Student, on_delete=None)
    obtained_marks = models.IntegerField(blank=True,null=True)

    class Meta:
        permissions = {
            ('can_view_result_faculty', 'can view result faculty'),
            ('can_view_result_student', 'can view result student')
        }


class AttainmentAL(models.Model):
    assessment_id = models.ForeignKey(Assessment, on_delete=None)
    co_id = models.ForeignKey(CourseOutcome, on_delete=None)
    attainment_per = models.FloatField()

    def __str__(self):
        return str(self.assessment_id) + self.co_id.text + ' ' + str(self.attainment_per)


class AttainmentCL(models.Model):
    co_id = models.ForeignKey(CourseOutcome, on_delete=None)
    year = models.PositiveSmallIntegerField()
    attainment = models.FloatField()


class AttainmentPL(models.Model):
    program = models.ForeignKey(Program, on_delete=None)
    po_id = models.ForeignKey(ProgramOutcome, on_delete=None)
    year = models.PositiveSmallIntegerField()
    attainment = models.FloatField()