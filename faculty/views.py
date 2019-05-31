from django.shortcuts import render,redirect
from django.contrib.auth.models import User, Group
from user.views import group_required
from .forms import FacultyRegistrationForm,FacultyRegistrationFormSubmit
from .models import Faculty
from student.models import Student
from django.contrib.auth.decorators import permission_required
from student.filters import StudentFilter
# Create your views here.


@permission_required('faculty.can_update_profile', login_url="user:register")
def updateFacultyProfile(request):
    if request.method == "POST":
        try:
            if request.user.faculty.submit is True:
                faculty_form = FacultyRegistrationFormSubmit(request.POST, instance=request.user.faculty)
            else:
                faculty_form = FacultyRegistrationForm(request.POST, instance=request.user.faculty)
        except:
            faculty_form = FacultyRegistrationForm(request.POST)

        if faculty_form.is_valid():
            fprofile = faculty_form.save(commit=False)
            fprofile.user = request.user
            if 'Submit' in request.POST:
                faculty_group = Group.objects.get(name='Faculty')
                request.user.groups.add(faculty_group)
                fprofile.submit = True
            fprofile.save()
        return redirect('faculty:register')

    else:
        try:
            if request.user.faculty.submit is True:
                faculty_form = FacultyRegistrationFormSubmit(instance=request.user.faculty)
            else:
                faculty_form = FacultyRegistrationForm(instance=request.user.faculty)
        except:
            faculty_form = FacultyRegistrationForm()
    return render(request, 'faculty/updateFacultyForm.html', {'form': faculty_form})



def showFacultyList(request):
    detail = Faculty.objects.all()
    return render(request,'faculty/showfacultylist.html', {'detail': detail})


@permission_required('faculty.can_view_self_profile', login_url='user:register')
def viewProfileFaculty(request):
    faculty = Faculty.objects.get(user_id=request.user.id)
    return render(request, 'faculty/profile.html', {'faculty':faculty})


# Link in self profile
@permission_required('faculty.can_view_student_list', login_url="denied")
def student_list(request):
    student_list = Student.objects.all()
    stud_filter = StudentFilter(request.GET, queryset=student_list)
    return render(request, 'faculty/student_list.html', {'filter': stud_filter})
