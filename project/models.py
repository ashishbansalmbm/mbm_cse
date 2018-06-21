from django.db import models
from user.models import User


class Project(models.Model):
    title = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=2000,null=False)
    supervisor = models.CharField(max_length=300)
    duration = models.DurationField()
    funding_agency = models.CharField(max_length=100)
    amount = models.BigIntegerField(max_length=15)
    date_of_start = models.DateField(null=False)
    status = models.CharField(max_length=50, null=False)
    remarks = models.TextField()
    type = models.CharField(max_length=100)


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    team_name = models.CharField(max_length=500, null=True)

