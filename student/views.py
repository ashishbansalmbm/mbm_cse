from django.shortcuts import render
from .forms import StudentProfile, StudentProfileSubmit
from django.shortcuts import redirect
from .models import Student
from .filters import StudentFilter
from django.contrib.auth.decorators import permission_required, PermissionDenied
from django.contrib.auth.models import Group
from user.views import group_required
# Creating a Student Profile


@permission_required('student.can_update_profile', login_url="user:register")
def update(request):
    if request.method == 'POST':
            try:
                if request.user.student.submit:
                    form = StudentProfileSubmit(request.POST, instance=request.user.student)
                else:
                    form = StudentProfile(request.POST, instance=request.user.student)
            except:
                form = StudentProfile(request.POST)

            if form.is_valid():
                student = form.save(commit=False)
                if 'Submit' in request.POST:
                    student.submit = True
                student.user = request.user
                form.save()
                return redirect('student:update')
            context = {'form': form}
            return render(request, 'student/student_form.html', context)

    else:
        try:
            if request.user.student.submit:
                form = StudentProfileSubmit(instance=request.user.student)
                student = request.user.student
                context = {'form': form , 'student': student}
            else:
                form = StudentProfile(instance=request.user.student)
                context = {'form': form}
        except:
            form = StudentProfile()
            context = {'form': form}
        return render(request, 'student/student_form.html', context)


# Faculty Will have the link
@permission_required('student.faculty_can_view_student_profile', login_url="denied")
def profile(request, pk):
    student = Student.objects.get(pk=pk)
    return render(request, 'student/student_profile_detail.html', {'student': student})


@permission_required('student.can_view_student_list', login_url='denied')
def show_student_list(request):
    detail = Student.objects.all()
    stud_filter = StudentFilter(request.GET, queryset=detail)
    return render(request, 'student/show_student_list.html', {'filter': stud_filter})
