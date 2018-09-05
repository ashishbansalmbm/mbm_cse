from django.db import models
from department.models import Department


class Program(models.Model):
    name = models.CharField(max_length=150)
    duration = models.SmallIntegerField()
    department = models.ForeignKey(Department, on_delete=None)

    def __str__(self):
        return self.name

    class Meta:

        permissions = (
            ('can_view_program', 'can view program '),
            ('can_create_program', 'can create program'),
        )


class ProgramOutcome(models.Model):
    program = models.ForeignKey(Program, on_delete=None)
    text = models.TextField()
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title



class ProgramFeedback(models.Model):
    program = models.ForeignKey(Program, on_delete=None)
    year = models.DateField()
    active = models.BooleanField(default=False)
