"""from django.urls import path
from .import views

urlpatterns=[
path('', views.ProjectForm.as_view(), name='project_add'),
]"""
from django.conf.urls import url
from django.urls import path
from project import views

app_name = 'project'

urlpatterns = [
    # projects ideas
    path('', views.featured_projects, name='Home'),

    url(r'^index/$', views.IndexView, name='index'),

    url(r'^entry/$', views.ProjectEntry, name='project-entry'),

    url(r'^delete/(?P<ind>[0-9]+)/$', views.ProjectReport, name='project-delete'),

    url(r'^mentor/(?P<ind>[0-9]+)/$', views.ProjectMentor, name='project-mentor'),

    url(r'^description/(?P<ind>[0-9]+)/$', views.ProjectDescription, name='description'),

    url(r'^index/create-team/(?P<pro>[0-9]+)/$', views.ApplyTeamIndex, name='TeamIndex'),
    # mentored projects

    url(r'^create-team/$', views.ApplyTeam, name='ApplyTeam'),

    url(r'^create-team/member/$', views.receive, name='Auto'),

    # url(r'^mentoredproject/(?P<ind>[0-9]+)/ind/$',views.ApplyInd_MP,name='MP-ApplyInd'),

    # url(r'^create-team/(?P<ind>[0-9]+)/addmember/$', views.AddMemberToTeam, name='AddMember'),

    # url(r'^create-team/(?P<ind>[0-9]+)/addmember2/$', views.AddMemberToTeam2, name='AddMember2'),
    # academic projects
    url(r'^academicproject/$', views.AcademicProject, name='project-academic_project'),
    url(r'^academicproject/(?P<pro>[0-9]+)/$', views.ShowTeams, name='teamss'),
    url(r'^academicproject/(?P<pro>[0-9]+)/(?P<tid>[0-9]+)/$', views.ATeam, name='Ateamss'),
    # url(r'^academicproject/assignpro/$', views.AssignProject, name='assign_project'),
    url(r'^academicproject/applyforproject', views.ApplyForAcademicProject, name='applyforpro'),
    url(r'^academicproject/alloted', views.AllotApplied, name='allotapplied'),
    # myproject
    url(r'^myproject/$', views.MyProject, name='myProject'),

    url(r'^myproject/(?P<pk>[0-9]+)/update', views.UpdateStatusMyProject.as_view(), name='update-status'),

    url(r'^myproject/(?P<ind>[0-9]+)/viewteam', views.ViewProjectTeam, name='view-team'),

    url(r'^myproject/(?P<ind>[0-9]+)/viewreq', views.ViewProjectRequest, name='teamrequest'),

    url(r'^myproject/(?P<ind>[0-9]+)/(?P<ind2>[0-9]+)/approved', views.MemberApprove, name='member-approve'),

    url(r'^myproject/(?P<ind>[0-9]+)/(?P<ind2>[0-9]+)/disapproved', views.MemberDisapprove, name='member-disapprove'),

    url(r'^update/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project-update'),

    url(r'^verify/$', views.VerifyProject, name='verify'),

    url(r'^verify/approved/(?P<id>[0-9]+)/$', views.ProjectVerified, name='proverified'),

    url(r'^verify/disapproved/(?P<id>[0-9]+)/$', views.ProjectDisapproved, name='prodisapproved'),

    url(r'^teams/$', views.MyTeams, name='myteam'),
    # front office


]
