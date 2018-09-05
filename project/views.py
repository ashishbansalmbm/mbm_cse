# from django.views import generic
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from .models import Project, ProjectMember, Team
# from user.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .filters import UserFilter
from django.contrib.auth.models import User
from .forms import ProjectTeamForm, ProjectTeamForm2, ProjectEntryForm
from django.contrib import messages
from django.urls import reverse
from .filters import IndexFilter
import json
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@permission_required('project.can_view_project_list', login_url="denied")
def IndexView(request):
    project_list = IndexFilter(request.GET,queryset=Project.objects.all().order_by('status'))
    return render(request, 'ProjectIdeas/index.html', {'project_list': project_list})


# view for the product entry page
@permission_required('project.add_project', login_url="user:register")
def ProjectEntry(request):
    if request.method == 'POST':
        form = ProjectEntryForm(request.POST)
        if form.is_valid():
            xy = form.save(commit=False)
            obj = User.objects.get(id=request.user.id)
            #print(obj.username, "POST")
            xy.added_by = obj.username
            xy.save()
            return redirect(reverse('project:index'))
        else:
            form = ProjectEntryForm()
    else:
        form = ProjectEntryForm()
    return render(request, 'ProjectIdeas/project_form.html', {'form': form})
# success_url = reverse_lazy('project:index')

@permission_required('project.can_view_project_list', login_url="denied")
def ProjectDescription(request, ind):
    obj = Project.objects.get(pk=ind)
    return render(request, 'ProjectIdeas/description.html', {'obj': obj})


class ProjectUpdate(UpdateView):
    permission_required = "project.can_view_project_list"
    login_url = "denied"
    model = Project
    fields = ['description', 'type', 'resources', 'funding_agency', 'amount', 'status']
    template_name = 'ProjectIdeas/updateform.html'
    success_url = reverse_lazy('project:myProject')


@permission_required('project.can_mentor_project', login_url="denied")
def ProjectMentor(request, ind):
    obj = get_object_or_404(Project, pk=ind)
    if obj.type == 'IDEA':
        obj2 = Project()
        obj2.title = obj.title
        obj2.status = "OnGoing"
        obj2.description = obj.description
        obj2.duration = obj.duration
        obj2.amount = obj.amount
        obj2.date_of_start = obj.date_of_start
        obj2.remarks = obj.remarks
        obj2.resources = obj.resources
        obj2.max_number_ProjectMembers = obj.max_number_ProjectMembers
        obj2.funding_agency = obj.funding_agency
        obj2.type = "MNR"
        obj2.supervisor_id = request.user.id
        obj2.added_by = obj.added_by
        obj2.save()
        messages.success(request, 'Your record was saved successfully!')
    return HttpResponseRedirect('/project/index/')


@permission_required('project.can_report_project', login_url="denied")
def ProjectReport(request, ind):
     obj = get_object_or_404(Project, pk=ind)
     obj.report = True
     obj.save()
     return HttpResponseRedirect('/project/index/')


# academic project
# show project list for allotment from projects created by respective faculty
@permission_required('project.can_allot_projects', login_url="denied")
def AcademicProject(request):
    uid = request.user.username
    A_pro_list = Project.objects.raw("select * from project_project where project_project.type='IDEA'"
                                     " and project_project.report=0 and added_by=%s and status='OnGoing' and "
                                     "project_project.id not in "
                              "(select project_id from project_team where project_id is not NULL)",[uid])

    return render(request,'AcademicProjects/AcademicProjectList.html',{'A_pro_list': A_pro_list})

# show teams for allotment
@permission_required('project.can_allot_projects', login_url="denied")
def ShowTeams(request,pro):
    teams = Team.objects.raw("select project_team.team_id,project_team.team_name,project_team.team_leader_id,"
                             "project_team.id from project_team where project_team.project_id is NULL")
    return render(request, 'AcademicProjects/teams(assign).html', {'teams': teams, 'pro': pro})

# allotment of project
@permission_required('project.can_allot_projects', login_url="denied")
def ATeam(request, pro, tid):
    obj = Team.objects.get(id=tid)
    obj.project = Project.objects.get(id=pro)
    obj.save()
    return HttpResponseRedirect('/project/academicproject/')

""" 
def AssignProject(request):
    #team_list = Team.objects.all()
    team_list = Team.objects.raw("select project_team.team_id,project_team.team_name,project_team.team_leader,
    project_team.id "
                                 "from project_team where project_team.project_id is NULL")
    project_list = Project.objects.filter(type="IDEA")
    alllist = {'team_list': team_list, 'project_list': project_list}
    if request.method == 'POST':
        allproject = request.POST.getlist('pro')
        allteamid = request.POST.getlist('teamid')
        i = 0
        for obj2 in allproject:

            form = AssignProjectForm(request.POST)
            if form.is_valid():
                xy = Team.objects.get(team_id=allteamid[i])
                xy.project = Project.objects.get(id=allproject[i])
                xy.save()
                i += 1
            else:
                return HttpResponse('FORM IS NOT VALID')
        return redirect('/project/academicproject/')
    else:
         form = AssignProjectForm()
    return render(request, 'AcademicProjects/AssignProject.html',{'form': form, 'team_list': team_list , 'project_list': project_list})
"""
    #return render(request, 'AcademicProjects/AssignProject.html', {'team_list': team_list, 'project_list': project_list})


@permission_required('project.can_verify_projects', login_url="denied")
def VerifyProject(request):
    f_id=request.user.id
    team_list = User.objects.raw("select project_project.title, project_team.team_name,project_project.id, "
                                 "project_team.team_leader_id"
                                 ",project_project.resources from project_project ,project_team "
                                 "where project_project.id=project_team.project_id and project_project.type='ACA_V' and "
                                 "project_project.report=0")
    return render(request, 'myprojects/verifyproject.html', {'team_list': team_list})


@permission_required('project.can_verify_projects', login_url="denied")
def ProjectVerified(request,id):
    obj = Project.objects.get(pk=id)
    obj.type = "ACA_A"
    obj.save()
    return render(request,'myprojects/verifyproject.html')


@permission_required('project.can_verify_projects', login_url="denied")
def ProjectDisapproved(request,id):
    obj = Project.objects.get(pk=id)
    obj.type = "IDEA"
    obj.remarks = "REJECTED FROM ACADEMIC PROJECTS"
    obj.save()
    return render(request,'myprojects/verifyproject.html')


@permission_required('project.can_view_self_project', login_url="denied")
def MyProject(request):
    my_pro_added =    Project.objects.raw("select * from project_project where added_by=%s;", [request.user.username])
    my_pro_supervisor = Project.objects.raw("select * from project_project where project_project.supervisor_id=%s ", [request.user.id])
    my_pro_member = Project.objects.raw("select * from project_project where id in( select project_id from project_projectmember"
                                        ",project_team where project_projectmember.user_id=%s and project_team.id"
                                        "= project_projectmember.team_id_id)",[request.user.id])
    return render(request, 'myprojects/viewall.html', {'obj': my_pro_supervisor, 'obj2': my_pro_member, 'obj3': my_pro_added})


class UpdateStatusMyProject(UpdateView):
    login_url = "denied"
    permission_required = "can_view_self_project"
    model = Project
    template_name = 'myprojects/UpdateStatus.html'
    fields = {'status',}
    success_url = reverse_lazy('project:myProject')


@permission_required('project.can_view_team', login_url="denied")
def ViewProjectTeam(request,ind):
    # obj = ProjectMember.objects.filter(project=ind)
    # query_set2 = User.objects.filter(user_name=obj.user)
    query_set3 = User.objects.raw(" select * from auth_user,project_projectmember where auth_user.id = "
                                  " project_projectmember.user_id and project_projectmember.team_id_id=%s and "
                                  " project_projectmember.membership= 1", [ind])
    return render(request, 'myprojects/ViewTeam.html', {'obj2': query_set3, })


def ViewProjectRequest(request, ind):
    xy = Team.objects.get(id=ind)
    tl = xy.team_leader.id
    uid = request.user.id
    if (uid == uid):
        query_set2 = User.objects.raw("select auth_user.id, auth_user.first_name,auth_user.last_name"
                                      " from auth_user, "
                                      " project_projectmember where project_projectmember.team_id_id=%s and "
                                      " auth_user.id=project_projectmember.user_id and  project_projectmember.membership = 0",
                                      [ind])
        return render(request, 'myprojects/MemberRequest.html', {'obj': query_set2, 'ind': ind, })
    else:
        return HttpResponseRedirect('/denied/')

# req user id and team id and delete it
def MemberDisapprove(request, ind, ind2):
    xy = Team.objects.get(id=ind2)
    tl = xy.team_leader.id
    uid = request.user.id
    if (tl == uid):
        obj = ProjectMember.objects.get(user=ind, team_id=ind2)
        obj.delete()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/denied/')


# req user id and team id
def MemberApprove(request, ind, ind2):
    xy = Team.objects.get(id=ind2)
    tl = xy.team_leader.id
    uid = request.user.id
    if (tl == uid ):
        obj = ProjectMember.objects.get(user=ind, team_id=ind2)
        obj.membership = True
        obj.save()
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect('/denied/')


@permission_required('project.can_view_project_list', login_url="denied")
def ApplyTeam(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectTeamForm(request.POST)
        try:
            obj2 = request.POST['receiver_id']
            obj2 = obj2.split(',')
        except MultiValueDictKeyError:
            obj2 = False
        #length = len(obj2)
        i = 0
        if obj2:
            if form.is_valid():
                team = form.cleaned_data.get('team_id')
                form.save()
            for mem in obj2:
                x = ProjectMember()
                x.user = User.objects.get(id=obj2[i])
                x.team_id = Team.objects.get(team_id=team)
                x.save()
                i = i+1
            return redirect(reverse('project:index'))
        else:
            form = ProjectTeamForm()
    else:
        form = ProjectTeamForm()
    return render(request, 'MentoredProject/ApplyAsTeam.html', {'form': form})


@permission_required('project.can_view_project_list', login_url="denied")
def ApplyTeamIndex(request, pro):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ProjectTeamForm2(request.POST)
        try:
            obj2 = request.POST['receiver_id']
            obj2 = obj2.split(',')
        except MultiValueDictKeyError:
            obj2 = False
        # length = len(obj2)
        i = 0
        if obj2:
            if form.is_valid():
                team = form.cleaned_data.get('team_id')
                abc = form.save(commit=False)
                abc.project = Project.objects.get(id=pro)
                abc.save()
            for mem in obj2:
                x = ProjectMember()
                x.user = User.objects.get(id=obj2[i])
                x.team_id = Team.objects.get(team_id=team)
                x.save()
                i = i + 1
            return redirect(reverse('project:index'))
        else:
            form = ProjectTeamForm2()
    else:
        form = ProjectTeamForm2()
    return render(request, 'MentoredProject/ApplyAsTeam.html', {'form': form})

def receive(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        users = User.objects.filter(first_name__icontains=q)
        results = []
        for i in users:
            users_json = {}
            users_json['label'] = i.first_name + " " + i.last_name + " -" + i.username
            users_json['value'] = i.first_name + " " + i.last_name
            users_json['id'] = i.id
            results.append(users_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def MyTeams(request):
    obj=Team.objects.raw("select * from project_team where project_team.team_leader_id=%s",[request.user.id])
    return render(request,'myprojects/MyTeams.html',{'obj': obj, })


def featured_projects(request):
    obj = Project.objects.raw("select * from project_project where featured=1 order by title ")
    return render(request, 'frontoffice/featuredprojects.html', {'obj': obj})


def ApplyForAcademicProject(request):
    obj = User.objects.get(id=request.user.id)
    # print(obj.username)
    pro = Project.objects.raw("select * from project_project where project_project.type='ACA_V'"
                              "  order by title and added_by=%s ", [obj.username])
    teams = Team.objects.raw(" select * from project_team where project_team.team_leader_id = %s "
                            " and project_team.project_id is NULL", [request.user.id])
    return render(request, 'AcademicProjects/applyAPstudents.html', {'pro': pro, 'teams': teams})

#allot academic project selected by individual
#@permission_required('project.can_view_project_list', login_url="denied")
def AllotApplied(request):
    pro = request.POST.get('pallot')
    t = request.POST.get('tallot')
    # print(pro)
    # print(t)
    obj = Team.objects.get(id=t)
    obj.project = Project.objects.get(id=pro)
    obj.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))