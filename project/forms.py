from .models import ProjectMember, Team, Project
from django.forms import ModelForm, formset_factory
from django import forms


class ProjectTeamForm(ModelForm):
    class Meta:
        template_name = 'MentoredProject/ApplyAsTeam.html'
        model = Team
        fields = ['team_id', 'team_name', 'team_leader','project',]


class ProjectEntryForm(ModelForm):
    class Meta:
        template_name = 'ProjectIdeas/project_form.html'
        model = Project
        fields = ['title', 'description', 'type', 'supervisor', 'resources', 'duration', 'funding_agency',
                  'max_number_ProjectMembers', 'amount', 'date_of_start', 'status', 'remarks',]

class ProjectTeamForm2(ModelForm):
    class Meta:
        template_name = 'MentoredProject/ApplyAsTeam.html'
        model = Team
        fields = ['team_id', 'team_name', 'team_leader',]


class AddMemberToTeamForm(ModelForm):
    class Meta:
        template_name = 'MentoredProject/AddNewMember.html'
        model = ProjectMember
        fields = ['user',]


class AssignProjectForm(ModelForm):
    class Meta:
        model = Team
        template_name = 'AcademicProject/AssignProject.html'
        fields = ['project', ]


class TeamMemberForm(forms.Form):
    #name = forms.CharField(
    #    label='Member Name',
    #    widget=forms.TextInput(attrs={
    #        'class': 'form-control',
    #        'placeholder': 'Enter Project Member Name here'
    #    })
    #)
    user_name = forms.CharField(label='Member name', max_length=100)
MemberFormset = formset_factory(TeamMemberForm, extra=1)