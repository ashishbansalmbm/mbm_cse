from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Course, CourseOutcome, CourseAvailable, CoPo, CourseProgram, CourseEnrollment, User
from program.models import ProgramOutcome, Program
from user.models import Profile
from .forms import Course_Form, CourseProg_Form, CourseOffer_Form, Enroll_Form
from program.forms import Course_Outcome_Form, CoPo_Link_Form
from django.contrib import messages
from django.db.models import Q
from enumerations.enum import Semester
from student.models import Student
from .filters import CourseFilter
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@permission_required('course.can_view_course', login_url="denied")
def IndexView(request):
    all_course = Course.objects.filter(deleted=False)
    sems = {d.name: d for d in Semester}
    progs = Program.objects.all()
    programs = []
    for course in all_course:
        pro = CourseProgram.objects.filter(course=course.id)
        ppp = ""
        for p in pro:
            ppp += str(p.program.name) + "/"
        ppp=ppp[0:-1]
        programs.append(ppp)
    query = CourseProgram.objects.filter(course__deleted=False)
    course_filter = CourseFilter(request.GET, queryset=query)
    abc = zip(all_course, programs)
    context = {"all_course": all_course,
               "sems": sems,
               "programs": programs,
               "progs": progs,
               "loop": abc,
               "filter": course_filter, }
    return render(request, 'course/index.html', context)


@permission_required('course.can_view_course', login_url="denied")
def DetailView(request, pk):
    course = get_object_or_404(Course, pk=pk)
    programs = CourseProgram.objects.filter(course=course.id)
    pro = ""
    # type = request.user.user_type
    type = 'F'
    for p in programs:
        pro += str(p.program.name) + " "

    context = {"course": course,
               "programs": programs,
               "type": type
               }
    return render(request, 'course/detail.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def CourseCreate(request):
    if request.method == "POST":
        course_form = Course_Form(request.POST)
        prog_form = CourseProg_Form(request.POST)

        if course_form.is_valid() and prog_form.is_valid():
            course = course_form.save()
            p = prog_form.save(commit=False)
            p.course = Course.objects.get(id=course.id)
            p.save()
            return redirect('course:index')

    else:
        course_form = Course_Form()
        prog_form = CourseProg_Form()

    context = {"course_form": course_form, "prog_form": prog_form, }
    return render(request, 'course/course_form.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def CourseUpdate(request, pk):
    instance = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        course_form = Course_Form(request.POST, instance=instance)
        if course_form.is_valid():
            course_form.save()
            return redirect('course:index')
    else:
        course_form = Course_Form(instance=instance)
    return render(request, 'course/course_form.html', {'course_form': course_form})


@permission_required('course.can_create_course_faculty', login_url="denied")
def CourseDelete(request, pk):
    instance = Course.objects.get(pk=pk)
    instance.deleted = True
    instance.save()
    return redirect('course:index')


def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']
        if srch:
            match = Course.objects.filter(Q(name__icontains=srch) |
                                          Q(course_code__icontains=srch) |
                                          Q(course_type__icontains=srch) |
                                          Q(semester__icontains=srch)
                                          )
            if match:
                return render(request, 'course/search.html', {'sr': match})
            else:
                print(srch)
                messages.error(request, 'no result found')
                return render(request, 'course/search.html', {'sr': match})
        else:
            return HttpResponseRedirect(reverse('course:index'))


@permission_required('course.can_create_course_faculty', login_url="denied")
def Add_CO(request, pk):
    if request.method == "POST":
        co_form = Course_Outcome_Form(request.POST)
        all_cos = CourseOutcome.objects.filter(course=pk)

        if co_form.is_valid():
            outcome = co_form.save(False)
            outcome.course = Course.objects.get(pk=pk)
            outcome = co_form.save()

            return redirect('course:po-select', co=outcome.id)

    else:
        co_form = Course_Outcome_Form
        course = Course.objects.get(pk=pk)
        all_cos = CourseOutcome.objects.filter(course=pk)

    context = {"co_form": co_form,
               "course": course,
               "all_cos": all_cos,
               }
    return render(request, 'course/co_form.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def Select_PO(request, co):
    no_pos = ProgramOutcome.objects.count()
    LinkFormSet = formset_factory(CoPo_Link_Form, max_num=no_pos - 1)
    outcome = CourseOutcome.objects.get(pk=co)
    course = Course.objects.get(id=outcome.course.id)
    all_pos = ProgramOutcome.objects.all()
    if request.method == "POST":
        # print("post")
        formset = LinkFormSet(request.POST)
        if (formset.is_valid()):
            # print("valid")
            for form in formset:
                link = form.save(False)
                if link.level != 'N':
                    link.course_outcome = outcome
                    link.user = request.user
                    link.save()
            return redirect('course:co-new', pk=course.pk)

    else:
        formset = LinkFormSet(initial=[{'program_outcome': x.id} for x in all_pos])

    context = {"formset": formset,
               "all_pos": all_pos,
               "outcome": outcome,
               "course": course, }
    return render(request, 'course/select_po.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def OfferCoursesIndex(request):
    av_courses = CourseAvailable.objects.filter(active=True)
    context = {"av_courses": av_courses, }
    return render(request, 'course/offered.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def OfferCourses(request):
    all_courses = Course.objects.filter(deleted=False)
    courseDict = {}
    for c in all_courses:
        programs = CourseProgram.objects.filter(course=c.id)
        program_list = ""
        for p in programs:
            program_list += str(p.program.id) + ";"
        courseDict[c.id] = {}
        courseDict[c.id]['name'] = c.name
        courseDict[c.id]['semester'] = c.semester
        courseDict[c.id]['code'] = c.course_code
        courseDict[c.id]['programdetails'] = program_list
    form = CourseOffer_Form()
    progs = Program.objects.all()
    if request.method == "POST":
        course = request.POST.get('course')
        if not course:
            return HttpResponse('<p>("You Have To select a course")</p>')
        crse = Course.objects.get(id=course)
        year = request.POST.get('year')
        if not year:
            return HttpResponse('Please enter a valid year')

        offCourses = CourseAvailable.objects.filter(course=crse.id, year=year).count()
        print(crse.id)
        print(offCourses)
        if offCourses == 0:
            off_course = form.save(commit=False)
            off_course.course = crse
            off_course.faculty = request.user
            off_course.year = year
            off_course.save()
        else:
            return HttpResponse('Already offered!')
        return redirect('course:course-offeredlist')
    sems = {d.name: d for d in Semester}
    context = {"all_courses": courseDict,
               "progs": progs, 'sems': sems}
    return render(request, 'course/offer.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def Enroll_Student(request, ca_id):
    students = Student.objects.all()
    courses = CourseAvailable.objects.get(id=ca_id)
    year = courses.year
    crse = Course.objects.get(id=courses.course.id)
    sem = crse.semester
    pro = CourseAvailable.objects.raw(
        "select * from course_courseavailable, course_courseprogram where course_courseavailable.id=%s and "
        " course_courseprogram.course_id = course_courseavailable.course_id", [ca_id])
    sten = CourseEnrollment.objects.filter(year=year, course=crse)

    student_list = []
    for pro_obj in pro:
        # prog = Program.objects.get(id=pro_obj.program)
        student = Student.objects.filter(program=pro_obj.program_id, semester=sem)
        for student_obj in student:
            if not CourseEnrollment.objects.filter(student=student_obj.user.id, year=year, course=crse):
                student_list.append(student_obj)
    context = {"students": student_list,
               "senrolled": sten, }
    if request.method == "POST":
        # m = []
        m = request.POST.getlist('student')
        for i in m:
            obj = CourseEnrollment()
            obj.student = User.objects.get(id=i)
            obj.year = year
            obj.course = crse
            obj.save()
        display = 1
        title = 'Done!!'
        message = 'Your Enrollment Was Successful!!'
        context = {'display': display, 'message': message, 'title': title,
                   "students": student_list, "courses": CourseAvailable.objects.filter(faculty=request.user)}
        return render(request, 'course/mycourses-f.html', context)
    return render(request, 'course/enroll-student.html', context)


@permission_required('course.can_view_mycourse_faculty', login_url="denied")
def My_Course_Faculty(request):
    courses = CourseAvailable.objects.filter(faculty=request.user)
    context = {"courses": courses}
    return render(request, 'course/mycourses-f.html', context)


@permission_required('course.can_view_mycourse_student', login_url="denied")
def My_Course_Student(request):
    courses = CourseEnrollment.objects.filter(student=request.user.id)
    print(request.user.profile.id)
    print(courses)
    course_list = []
    for c in courses:
        course_list.append(c.course)
    print(course_list)
    context = {"course_list": course_list,
               }
    return render(request, 'course/mycourses-s.html', context)


@permission_required('course.can_create_course_faculty', login_url="denied")
def See_Links(request, co):
    outcome = CourseOutcome.objects.get(pk=co)
    po_links = CoPo.objects.filter(course_outcome=outcome.id)
    context = {"po_links": po_links,
               "outcome": outcome,
               }
    retString=""
    for link in po_links:
        if link.level != 'N':
            retString +=str(link.program_outcome) + '-'
            if link.level == 'H':
                retString+='High'
            elif link.level == 'S':
                retString+='Slight'
            elif link.level == 'M':
                retString +='Minimum'
            retString+='<br >'
    return HttpResponse(retString)
    #return render(request, 'course/see_links.html', context)
