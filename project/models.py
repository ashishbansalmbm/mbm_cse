from django.db import models
from user.models import User
from django.urls import reverse
from enum import Enum


class Type(Enum):
    RS = "RESEARCH SPONSORED"
    CSY = "CONSULTANCY"
    IDEA = "IDEA"
    MNR = "MENTORED"
    ACA_V = "ACADEMIC VOLUNTARY"
    ACA_A = "ACADEMIC ALLOTTED"
    SMR = "SEMINAR"


class STATUS(Enum):
    Completed = "COMPLETED"
    OnGoing = "ON GOING"
    Restricted = "RESTRICTED"


class Project(models.Model):
    title = models.CharField(max_length=50, null=False)
    added_by = models.CharField(max_length=500)
    description = models.TextField(null=False)
    supervisor = models.ForeignKey(User, on_delete=None, blank=True, null=True)
    duration = models.DurationField()
    funding_agency = models.CharField(max_length=100)
    amount = models.BigIntegerField()
    date_of_start = models.DateField(null=False)
    status = models.CharField(max_length=50,  choices=[(tag.name, tag.value) for tag in STATUS])
    remarks = models.TextField()
    type = models.CharField(max_length=30, choices=[(tag.name, tag.value) for tag in Type])
    resources = models.CharField(max_length=1000)
    max_number_ProjectMembers = models.IntegerField()
    featured = models.BooleanField(default=False)
    report = models.BooleanField(default=False)

    class Meta:
        unique_together = ('added_by', 'title', 'supervisor',),
        permissions = (
            ('can_view_project_list', 'can view project list'),
            ('can_mentor_project','can mentor project'),
            ('can_report_project', 'can report project'),
            ('can_allot_projects', 'can allot project'),
            ('can_verify_projects', 'can verify project'),
            ('can_view_self_project','can view self project'),



        )


    def get_absolute_url(self):
        return reverse('project:index', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class Team(models.Model):
    team_name = models.CharField(max_length=500, null=True)
    team_leader = models.ForeignKey(User,on_delete=None)
    project = models.ForeignKey(Project, on_delete=None, blank=True, null=True)

    class Meta:
        permissions = (
            ('can_view_team', 'can view team'),
        )

    def __str__(self):
        return self.team_name


class ProjectMember(models.Model):
    user = models.ForeignKey(User, on_delete=None)
    team_id = models.ForeignKey(Team, on_delete=None)
    membership = models.BooleanField(default=False)

    def __str__(self):
        return self.user.get_full_name()

    class Meta:
        unique_together = ('user', 'team_id',)
