from django.contrib.auth.decorators import permission_required, PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.edit import UpdateView
from .models import Assessment, AssessmentQuestion, AssessmentResult, AttainmentAL, AttainmentPL, AttainmentCL
from django.urls import reverse
from .forms import ResultForm,QuestionForm, AssessmentForm, ResultFacultyForm, Calculate
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from student.models import Student
from program.models import Program, ProgramOutcome
from course.models import Course,CourseEnrollment, CourseProgram, CourseOutcome, CourseAvailable
from enumerations.enum import Semester
from .filters import UserFilter
from django.db.models import Sum, Q
from statistics import mean
import statistics


#@permission_required('assessment.can_view_assessment', login_url='denied')
class IndexView(PermissionRequiredMixin ,generic.ListView):
    permission_required = 'assessment.can_view_assessment'
    template_name = 'assessment/index.html'
    context_object_name = 'assessment_list'
    def get_queryset(self):
        return Assessment.objects.all()


@permission_required('assessment.can_view_assessment', login_url='denied')
def detail(request, pk):
    if 'submit_assessment' in request.POST:
        assessment_obj = Assessment.objects.get(id=pk)
        assessment_obj.assessment_completed = True
        assessment_obj.save()
        return HttpResponseRedirect(reverse('assessment:index'))
    assessment = get_object_or_404(Assessment, pk=pk)

    myassessment = Assessment.objects.raw("select assessment_assessment.id from assessment_assessment,faculty_faculty"
                                          " where faculty_id=faculty_faculty.id"
                                          " and faculty_faculty.user_id=%s", [request.user.id])

    for i in myassessment:
        if int(pk) == int(i.id) and i.assessment_completed == False:
            return render(request, 'assessment/question.html', {'assessment': assessment})
    return HttpResponse('<p>you do not have permission</p>')



@permission_required('assessment.can_view_assessment', login_url='denied')
def assess_detail(request, pk):
    assessment = get_object_or_404(Assessment, pk=pk)
    return render(request, 'assessment/assess_detail.html', {'assessment': assessment})


@permission_required('assessment.add_assessment', login_url='denied')
def createassessment(request):
    if request.method == 'POST':
        form = AssessmentForm(request.POST or None)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return HttpResponseRedirect(reverse('assessment:detail',  args=(data.id,)))
    else:
        form = AssessmentForm()
    return render(request, 'assessment/assessment_form.html', {'form': form})



class AssessmentUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'assessment.change_assessment'
    login_url = 'denied'
    model = Assessment
    fields = ['course', 'assessment_type', 'start_date', 'duration', 'faculty', 'year']


class AssessmentQuestionUpdate(PermissionRequiredMixin ,UpdateView):
    permission_required = 'assessment.change_assessment'
    model = AssessmentQuestion
    fields = ['question_type', 'text', 'max_marks', 'question_order', 'marking_scheme', 'outcome']


@permission_required('assessment.change_assessment', login_url='denied')
def updateresult(request, ass_id):
    question = AssessmentQuestion.objects.raw("select * from assessment_assessmentquestion where "
                                              "assessment_id= %s order "
                                              "by question_order", [ass_id])
    students = Student.objects.raw("select student_student.id, student_student.user_id from "
                                   "student_student,course_courseenrollment,assessment_assessment where "
                                   "assessment_assessment.id = %s and assessment_assessment.course_id = "
                                   "course_courseenrollment.course_id "
                                   "and assessment_assessment.year =course_courseenrollment.year and "
                                   "student_student.user_id = course_courseenrollment.student_id ", [ass_id])

    if request.method == "POST":
        # to submit result finally and set the result_completed true
        if 'submit_result' in request.POST:
            assessment_obj = Assessment.objects.get(id=ass_id)
            assessment_obj.result_completed = True
            assessment_obj.save()
            return HttpResponseRedirect(reverse('assessment:index'))
        # to save the marks in database
        else:
            marks = {}
            stu = []
            que = []
            for obj1 in students:

                for obj2 in question:
                    stu.append(obj1.user_id)
                    que.append(obj2.id)
            # send this zip to form.py to create dynamic fields
            pack = zip(stu, que)

            for obj1 in students:
                for obj2 in question:
                    marks[obj1.user_id] = {}
                    # fetch marks from form
                    marks[obj1.user_id][obj2.id] = request.POST['obtained_marks' + str(obj1.user_id) + str(obj2.id)]
                    form = ResultForm(request.POST or None, pack=pack)
                    if form.is_valid():
                        post = AssessmentResult()
                        # if entry is not found in database then it create new otherwise rewrite the same
                        try:
                            asr = AssessmentResult.objects.get(student=obj1.id, question=obj2.id)
                            post.id = asr.id
                        except AssessmentResult.DoesNotExist:
                            print("")

                        post.student = Student.objects.get(pk=obj1.id)
                        post.question = AssessmentQuestion.objects.get(pk=obj2.id)
                        # if marks are not filled then by default blank will be saved in obtained_marks field
                        if marks[obj1.user_id][obj2.id] == "":
                            print("")
                        else:
                            post.obtained_marks = marks[obj1.user_id][obj2.id]
                        post.save()
                    else:
                        return HttpResponse('form is not valid')
            return redirect('assessment:index')
    else:
            # this list is for the finally submit the result
            assessment = []
            assessment.append(ass_id)
            stu = []
            que = []
            c = {}
            q = {}
            max_marks = []
            for s in students:
                c[s.user_id] = {}
                c[s.user_id]["name"]=s.user.get_full_name
                c[s.user_id]["marks"] = {}

                for ques in question:
                    stu.append(s.user_id)
                    que.append(ques.id)
                    q[ques.id] = ques.question_order
                    max_marks.append(ques.max_marks)
                    try:
                        obj= AssessmentResult.objects.get(student=s.id,question=ques.id)
                        # this is for if obtained_marks field in database is blank then it will show nothing in form
                        if obj.obtained_marks == None:
                            c[s.user_id]["marks"][ques.id] = ""
                        else:
                            c[s.user_id]["marks"][ques.id] = obj.obtained_marks
                    except AssessmentResult.DoesNotExist:
                        c[s.user_id]["marks"][ques.id] = ""
            # it is for dynamic creating field
            pack = zip(stu, que)
            form = ResultForm(request.GET, pack=pack)
            max_marks.reverse()
            myassessment = Assessment.objects.raw(
                "select assessment_assessment.id from assessment_assessment,faculty_faculty"
                " where faculty_id=faculty_faculty.id"
                " and faculty_faculty.user_id=%s", [request.user.id])

            for i in myassessment:
                if int(ass_id) == int(i.id) and i.result_completed == False:
                    return render(request, 'assessment/updateresult.html',
                                  {'form': form, 'students': c, 'questions': q, 'assessment': assessment,
                                   'marks': max_marks})

            return HttpResponse('<p>you do not have permission</p>')


@permission_required('assessment.add_assessmentquestion', login_url='denied')
def createquestion(request, assessment_id):
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.assessment = Assessment.objects.get(pk=assessment_id)
            post.save()
            return redirect('assessment:detail', pk=post.assessment_id)
    else:
        form = QuestionForm()
    return render(request, 'assessment/assessmentquestion_form.html', {'form': form})

@permission_required('assessment.can_view_assessment', login_url='denied')
def search(request):
    assessment_list = Assessment.objects.all().order_by('-id')
    assessment_filter = UserFilter(request.GET, queryset=assessment_list)
    return render(request, 'assessment/index.html', {'filter': assessment_filter})

@permission_required('assessment.can_view_result_student', login_url='denied')
def student_result_semesterwise(request):
    student_id = request.user.id
    sem = Course.objects.raw("select course_course.id,course_course.semester,course_courseenrollment.year"
                             " from course_course,"
                             "course_courseenrollment where course_courseenrollment.student_id = %s "
                             "and course_courseenrollment.course_id="
                             "course_course.id group by course_course.semester,course_courseenrollment.year",[student_id])
    # list p for adding sum of marks and list m for adding total marks
    p = []
    m = []
    for obj1 in sem:
        sum = 0
        totalmarks = 0
        for obj2 in CourseEnrollment.objects.raw("select * from course_courseenrollment,course_course where "
                                                 "student_id=%s and course_course.id = course_courseenrollment.course_id "
                                                 "and course_course.semester = %s and course_courseenrollment.year="
                                                 "%s", [student_id, obj1.semester, obj1.year]):

            for obj3 in Assessment.objects.raw("select * from assessment_assessment,course_courseenrollment where"
                                               " assessment_assessment.course"
                                               "_id = %s and course_courseenrollment.year=assessment_assessment.year "
                                               "and course_courseenrollment.student_id = %s"
                                               " and course_courseenrollment.course_id=assessment_assessment.course_id"
                                               " and course_courseenrollment.year=%s and "
                                               " assessment_assessment.result_completed=1" ,[obj2.course_id, student_id,obj1.year]):
                for obj4 in obj3.assessmentquestion_set.all():
                    totalmarks += obj4.max_marks
                    stu = Student.objects.get(user=student_id)
                    student = stu.id
                    for obj5 in AssessmentResult.objects.raw("select * from assessment_assessmentresult where"
                                                             " assessment_assessmentresult.student_id = %s and"
                                                             " assessment_assessmentresult.question_id = %s",
                                                             [student, obj4.id]):

                        sum += obj5.obtained_marks
        p.append(sum)
        m.append(totalmarks)
    m.reverse()
    pack1 = zip(sem, p)
    return render(request, 'assessment/selfresult.html', {'pack': pack1,'marks': m})


@permission_required('assessment.can_view_result_student', login_url='denied')
def student_result_coursewise(request, sem, year):
    student_id = request.user.id
    courses = CourseEnrollment.objects.raw("select * from course_courseenrollment, course_course where "
                                           "course_courseenrollment.student_id=%s and "
                                           "course_course.id=course_courseenrollment.course_id and "
                                           "course_course.semester=%s and course_courseenrollment.year=%s"
                                           "", [student_id,sem, year])
    # list for append sum marks
    p = []
    marks = []
    for obj1 in courses:
        sum = 0
        total_marks = 0
        for obj2 in Assessment.objects.raw("select * from assessment_assessment,course_courseenrollment where"
                                           " assessment_assessment.course"
                                           "_id = %s and course_courseenrollment.year=assessment_assessment.year "
                                           "and course_courseenrollment.student_id = %s and"
                                           " course_courseenrollment.course_id=assessment_assessment.course_id"
                                           " and assessment_assessment.year=%s and assessment_assessment.result_completed=1", [obj1.course_id, student_id,year]):
            for obj3 in obj2.assessmentquestion_set.all():
                total_marks += obj3.max_marks
                stu = Student.objects.get(user=student_id)
                student = stu.id
                for obj4 in AssessmentResult.objects.raw("select * from assessment_assessmentresult where"
                                                         " assessment_assessmentresult.student_id = %s and"
                                                         " assessment_assessmentresult.question_id = %s", [student, obj3.id]):

                    sum += obj4.obtained_marks


        p.append(sum)
        marks.append(total_marks)
    pack1 = zip(courses, p)
    marks.reverse()
    return render(request, 'assessment/selfcourse.html', {'result': p, 'pack': pack1,'marks':marks})


@permission_required('assessment.can_view_result_student', login_url='denied')
def student_result_assessmentwise(request, pk, year):
    student_id = request.user.id
    papers = Assessment.objects.raw("select * from assessment_assessment,course_courseenrollment where "
                                    "course_courseenrollment."
                                    "student_id=%s and course_courseenrollment.year=assessment_assessment.year and "
                                    "assessment_assessment.course_id"
                                    "=%s and  course_courseenrollment.course_id=assessment_assessment.course_id"
                                    " and course_courseenrollment.year=%s and assessment_assessment.result_completed=1", [student_id,pk, year])
    p = []
    marks = []
    for obj1 in papers:
        sum = 0
        total_marks = 0
        for obj2 in obj1.assessmentquestion_set.all():
            total_marks+=obj2.max_marks
            obj = Student.objects.get(user=student_id)
            student = obj.id
            for obj3 in AssessmentResult.objects.raw("select * from assessment_assessmentresult where"
                                                     " assessment_assessmentresult.student_id = %s and"
                                                     " assessment_assessmentresult.question_id = %s", [student, obj2.id]):
                sum += obj3.obtained_marks
        p.append(sum)
        marks.append(total_marks)
    marks.reverse()
    pack1 = zip(papers, p)
    return render(request, 'assessment/selfassessment.html', {'papers': papers, 'result': p, 'pack': pack1,'marks':marks})


@permission_required('assessment.can_view_result_student', login_url='denied')
def student_result_questionwise(request, pk):
    question = AssessmentQuestion.objects.raw("select * from assessment_assessmentquestion where "
                                              "assessment_id = %s order by question_order", [pk])
    p = []
    student_id = request.user.id
    stu = Student.objects.get(user=student_id)
    student = stu.id
    for obj in question:
        marks = AssessmentResult.objects.get(question=obj.id, student=student)
        sum = marks.obtained_marks
        p.append(sum)
    pack1 = zip(question, p)
    return render(request, 'assessment/questionresult.html', {'pack': pack1})



def faculty_request(request):
    if request.method == "POST":
        form = ResultFacultyForm(request.POST)
        for i in form:
            print(i)
        if form.is_valid():
            program_obj = form.cleaned_data['program']
            semester_obj = form.cleaned_data['semester']
            year_obj = form.cleaned_data['year']
            #print(program_obj)
            #print(semester_obj)
            #print(year_obj)
            request.session['program_obj'] = program_obj
            request.session['semester_obj'] = semester_obj
            request.session['year_obj'] = year_obj
            return redirect('assessment:faculty_result')
    else:
        form = ResultFacultyForm()
        programs = Program.objects.all()
        semester = {}
        for s in Semester:
            semester[s.name] = s.value
        return render(request, 'assessment/select_program.html', {'programs': programs, 'sems' : semester })


def get_years_for_program(request):
    if request.method == "GET":
        program_id = request.GET.get("p")
        semester = request.GET.get("s")
        year = []
        if program_id and semester:

            ys=Assessment.objects.raw("select * from assessment_assessment where course_id in "
                                      "(select course_course.id from course_course inner join course_courseprogram on "
                                      "course_course.id=course_courseprogram.course_id where "
                                      "course_courseprogram.program_id=%s and course_course.semester=%s)",[program_id, semester])
            print(ys)
            for year_obj in ys:
                if year_obj.year not in year:
                    year.append(year_obj.year)
            print(year)
            return JsonResponse(year, safe=False)
        else:
            return JsonResponse(["error"], safe=False)


@permission_required('assessment.can_view_result_faculty', login_url='denied')
def result_faculty(request):
    program_obj = request.session.get('program_obj')
    semester_obj = request.session.get('semester_obj')
    year_obj = request.session.get('year_obj')
    #print('program_obj', program_obj)
    #print('semester_obj', semester_obj)
    #print('year_obj', year_obj)
    Students = Student.objects.raw("select distinct student_student.id from student_student, course_course, course_courseenrollment where student_student.program_id =%s and course_course.semester =%s "
                                   "and course_course.id=course_courseenrollment.course_id and course_courseenrollment.year=%s", [program_obj, semester_obj, year_obj])
    p = []
    l = []
    max_marks = []
    for Student_obj in Students:
        for Course_obj in Course.objects.raw("select course_course.id from course_course, course_courseprogram, course_courseenrollment "
                                             "where course_courseprogram.program_id = %s and course_course.id=course_courseenrollment.course_id and "
                                             "course_courseenrollment.student_id=%s and course_course.id=course_courseprogram.course_id and "
                                             "course_course.semester = %s", [program_obj, Student_obj.user_id, semester_obj]):
            sum = 0
            marks = 0
            if Course_obj not in l:
              l.append(Course_obj)
            #print("Course_obj",Course_obj.id)
            #print("student",Student_obj.student_id)
            for Assessment_obj in Assessment.objects.raw("select assessment_assessment.id from assessment_assessment,course_courseenrollment "
                                                         "where course_courseenrollment.student_id=%s and "
                                                         "assessment_assessment.course_id=%s and assessment_assessment.year=%s and "
                                                         "assessment_assessment.year=course_courseenrollment.year "
                                                         "and assessment_assessment.course_id=course_courseenrollment.course_id", [Student_obj.user_id,Course_obj.id,year_obj]):
                print("Assessment_id", Assessment_obj.id)
                for Question_obj in Assessment_obj.assessmentquestion_set.all():
                    marks += Question_obj.max_marks
                    var1 = Student.objects.get(user=Student_obj.user_id)
                    var2 = var1.id
                    for Result_obj in AssessmentResult.objects.raw("select *from assessment_assessmentresult where "
                                                                   "assessment_assessmentresult.student_id = %s and "
                                                                   "assessment_assessmentresult.question_id = %s", [var2, Question_obj.id]):
                        print("obtained marks",Result_obj.obtained_marks)
                        sum += Result_obj.obtained_marks
            p.append(sum)
            max_marks.append(marks)
    p.reverse()
    max_marks.reverse()
    return render(request, 'assessment/result_faculty.html', {'l': l, 'students': Students, 'p': p,'marks': max_marks})


@permission_required('assessment.can_view_result_faculty', login_url='denied')
def result_course(request, c_id):
    program_obj = request.session.get('program_obj')
    semester_obj = request.session.get('semester_obj')
    year_obj = request.session.get('year_obj')
    #print('program_obj', program_obj)
    #print('semester_obj', semester_obj)
    #print('year_obj', year_obj)
    Students = Student.objects.raw("select distinct student_student.id from student_student, course_course, course_courseenrollment where student_student.program_id =%s and course_course.semester =%s "
                                   "and course_course.id=course_courseenrollment.course_id and course_courseenrollment.year=%s",[program_obj, semester_obj, year_obj])
    p = []
    l = []
    max_marks = []
    for student_obj in Students:
        for assessment_obj in Assessment.objects.raw("select assessment_assessment.id from assessment_assessment,course_courseenrollment "
                                                     "where course_courseenrollment.student_id=%s and "
                                                     "assessment_assessment.course_id=%s and assessment_assessment.year=%s and "
                                                     "assessment_assessment.year=course_courseenrollment.year "
                                                     "and assessment_assessment.course_id=course_courseenrollment.course_id "
                                                     "order by assessment_assessment.start_date", [student_obj.user_id,c_id,year_obj]):
            sum = 0
            marks = 0
            #print('assessment_object', assessment_obj.id)
            if assessment_obj not in l:
                l.append(assessment_obj)
            for Question_obj in assessment_obj.assessmentquestion_set.all():
                marks += Question_obj.max_marks
                var1 = Student.objects.get(user=student_obj.user_id)
                var2 = var1.id
                for Result_obj in AssessmentResult.objects.raw("select *from assessment_assessmentresult where "
                                                               "assessment_assessmentresult.student_id = %s and "
                                                               "assessment_assessmentresult.question_id = %s",
                                                               [var2, Question_obj.id]):
                    # print("raj",Result_obj.obtained_marks)
                    sum += Result_obj.obtained_marks
            p.append(sum)
            max_marks.append(marks)
    p.reverse()
    max_marks.reverse()
    return render(request, 'assessment/result_faculty_course.html', {'l': l, 'students': Students, 'p': p, 'marks': max_marks})


@permission_required('assessment.can_view_result_faculty', login_url='denied')
def result_assessment(request, assess_id):
    program_obj = request.session.get('program_obj')
    semester_obj = request.session.get('semester_obj')
    year_obj = request.session.get('year_obj')
    Students = Student.objects.raw("select distinct student_student.id from student_student, course_course, course_courseenrollment where student_student.program_id =%s and course_course.semester =%s "
                                   "and course_course.id=course_courseenrollment.course_id and course_courseenrollment.year=%s",[program_obj, semester_obj, year_obj])
    p = []
    l = []
    marks_obj = []
    for student_obj in Students:
        for question_obj in AssessmentQuestion.objects.raw("select *from assessment_assessmentquestion where "
                                                           "assessment_assessmentquestion.assessment_id=%s",[assess_id]):
            que_marks = AssessmentQuestion.objects.get(id=question_obj.id)
            var_marks = que_marks.max_marks
            if question_obj not in l:
                l.append(question_obj)
            marks_obj.append(var_marks)
            #print('question_obj', question_obj.id)
            var1 = Student.objects.get(user=student_obj.user_id)
            var2 = var1.id
            marks = AssessmentResult.objects.get(question=question_obj.id, student=var2)
            sum = marks.obtained_marks

            p.append(sum)
    p.reverse()
    marks_obj.reverse()
    return render(request, 'assessment/result_faculty_assessment.html', {'l': l, 'students': Students, 'p': p, 'marks': marks_obj})


@permission_required('assessment.can_view_result_faculty', login_url='denied')
def result_student(request, stu_id):
    program_obj = request.session.get('program_obj')
    semester_obj = request.session.get('semester_obj')
    year_obj = request.session.get('year_obj')
    Courses = Course.objects.raw("select *from course_course, course_courseenrollment,course_courseprogram where "
                                 "course_courseprogram.program_id = %s and course_course.id=course_courseenrollment.course_id and "
                                 "course_courseenrollment.student_id=%s and course_course.id=course_courseprogram.course_id and "
                                 "course_course.semester = %s", [program_obj,stu_id,semester_obj])
    p = []
    l = []
    x = []
    marks_obj = []
    for course_obj in Courses:
        count = 0
        for assessment_obj in Assessment.objects.raw("select * from assessment_assessment,course_courseenrollment "
                                                     "where course_courseenrollment.student_id=%s and "
                                                     "assessment_assessment.course_id=%s and assessment_assessment.year=%s and "
                                                     "assessment_assessment.year=course_courseenrollment.year "
                                                     "and assessment_assessment.course_id=course_courseenrollment.course_id", [stu_id,course_obj.id,year_obj]):
            count = count+1
            if assessment_obj not in l:
                l.append(assessment_obj.id)
            #print('assessment ', assessment_obj.id)
            sum = 0
            total_marks = 0
            for Question_obj in AssessmentQuestion.objects.raw("select *from assessment_assessmentquestion where "
                                                               "assessment_assessmentquestion.assessment_id=%s",[assessment_obj.id]):
                total_marks += Question_obj.max_marks
                var1 = Student.objects.get(user=stu_id)
                var2 = var1.id
                for result_obj in AssessmentResult.objects.raw("select *from assessment_assessmentresult where "
                                                               "assessment_assessmentresult.student_id=%s and "
                                                               "assessment_assessmentresult.question_id=%s", [var2, Question_obj.id]):
                    sum += result_obj.obtained_marks
            p.append(sum)
            marks_obj.append(total_marks)
        x.append(count)
    #print(p)
    #print('list',x)
    y = max(x)
    #print('y', y)
    p.reverse()
    marks_obj.reverse()
    new_list = []
    for i in range(1,y+1):
        new_list.append(i)
    return render(request, 'assessment/result_faculty_student.html', {'l': l, 'courses': Courses, 'p': p, 'new_list': new_list, 'marks': marks_obj})

def search_or_calculate(request):
    if request.method == 'POST':
        print("form is fine")
        #form = Calculate(data=request.POST)
        #if form.is_valid():
        print('hey here')
        course_for_search = request.POST['course']
        year_for_search = request.POST['year']
        # if attainment for that result exit than forward to other page

        cond_1_existence = Q(co_id__course_id=course_for_search)
        cond_2_existence = Q(assessment_id__year=year_for_search)
        check_for_existence_of_course_attainment = AttainmentAL.objects.filter(cond_1_existence & cond_2_existence)
        request.session['course_for_search'] = course_for_search
        request.session['year_for_search'] = year_for_search

        if check_for_existence_of_course_attainment.exists():# course av but cal
            # msg this attainment alreay exists do you want to calculate again
            # if yes forward to function -> attainment_calculate
            # else redirect back to search page
            print("This was printed")
            return render(request,'assessment/attainment_exists.html') # pop up
        else: # course av but not cal
            # if doesn't exit than direct forward to function->attainment_calculate
            print("The else was printed")
            url = request.build_absolute_uri(reverse('assessment:attainment-cal'))

            return HttpResponse(url)

    else:
        form = Calculate()

    return render(request, 'assessment/search_for_attainment_per_course.html', {'form': form})


def get_valid_years(request):
    if request.is_ajax():
        course_for_search = request.GET.get('cid',None)
        course_for_search2 = request.GET.get('course',None)
        course_for_search3 = request.GET.get('year',None)
        print(course_for_search)

        print("hello")
        r_years = CourseAvailable.objects.filter(course=course_for_search)
        years =[]
        if r_years.exists():
            for obj in r_years:
                years.append(obj.year)
            return  JsonResponse(years,safe=False)
        else:
            err = ["error"]
            return JsonResponse(err,safe=False)

    # all year related to a course


def attainment_calculate(request):
    course_for_search = request.session.get('course_for_search')
    year_for_search = request.session.get('year_for_search')
    cond_1_ass = Q(course__id=course_for_search)
    cond_2_ass = Q(year=year_for_search)
    related_assignment = Assessment.objects.filter(cond_1_ass & cond_2_ass)
    total_related_assignment = related_assignment.count()

    course_outcomes = CourseOutcome.objects.filter(course__id = course_for_search)###

    for i in related_assignment:
        questions_in_i_th_assessment = AssessmentQuestion.objects.filter(assessment=i.id)
        per_outcome_question_marks = {} #

        for oc in course_outcomes:
            per_outcome_question_marks.update({oc.id: []})

        for q in questions_in_i_th_assessment:
            total_student = AssessmentResult.objects.filter(question=q.id).count()
            total_gain_marks = AssessmentResult.objects.filter(question=q.id).aggregate(s=Sum('obtained_marks'))['s'] # return a dict with s ke
            avg_marks = (total_gain_marks)/(total_student*(q.max_marks))

            for oc in course_outcomes:
                condition_1 = Q(id=q.id)
                condition_2 = Q(outcome__id=oc.id)

                check_for_match = AssessmentQuestion.objects.filter(condition_1 & condition_2)
                # matched
                print('oc, q', oc,q.id)
                print('check_for_match', check_for_match)
                if check_for_match.exists():
                    per_outcome_question_marks[oc.id].append(avg_marks)


        for oc in course_outcomes:
            try:
                per_outcome_question_marks[oc.id] = mean(per_outcome_question_marks[oc.id])
            except statistics.StatisticsError:
                per_outcome_question_marks[oc.id] = 0
            obj, created = AttainmentAL.objects.update_or_create(assessment_id=i, co_id=oc
                                                                 , defaults={
                    'attainment_per':per_outcome_question_marks[oc.id], })

    # in a new function
    l_for_marks = []
    # for a assessment complete
    for out in course_outcomes:
        for ass in related_assignment:
            m_cond_1 = Q(co_id_id=out.id)
            m_cond_2 = Q(assessment_id_id = ass.id)
            query_for_marks = AttainmentAL.objects.get(m_cond_1 & m_cond_2)
            required_marks = query_for_marks.attainment_per
            l_for_marks.append(required_marks)
    l_for_marks.reverse()

    # now for table AttainmentCL fill the value
    # pass values in function co_id, year_for_search, marks =??
    feed_attainment_cl_table(course_for_search, year_for_search) # $$$$$$$$$$$$$$$$$$$$$$$$
    return render(request, 'assessment/attainment_cal.html', {'outcomes': course_outcomes,
                                                              'assessment': related_assignment,
                                                              'att': l_for_marks,
                                                              'count':range(1,total_related_assignment+1) })

def feed_attainment_cl_table(course, year):
    course_needed = course
    year_needed = year
    course_outcomes = CourseOutcome.objects.filter(course__id=course_needed)
    cond_1 = Q(assessment_id__year=year_needed)

    for oc in course_outcomes:
        cond_2 = Q(co_id=oc)
        query_for_marks = AttainmentAL.objects.filter(cond_1 & cond_2)
        marks = []

        for att_obj in query_for_marks:
            marks.append(att_obj.attainment_per)

        marks = mean(marks)
        obj, created = AttainmentCL.objects.update_or_create(co_id=oc,year=year_needed,
                                                             defaults={'attainment':marks, })
    # now feed program outcomes table
    course_obj_for_program = CourseProgram.objects.get(course=course_needed)
    program_required = course_obj_for_program.program
    feed_attainment_pl_table(program_required, year)

def feed_attainment_pl_table(program,year):
    program_needed = program
    year_needed = year
    program_outcomes = ProgramOutcome.objects.filter(program=program_needed)

    print(program_outcomes)
    cond_1 = Q(year=year_needed)

    for po in program_outcomes:
        query_for_marks = AttainmentCL.objects.filter(co_id__copo__program_outcome=po)
        print('query_for_marks', query_for_marks)
        marks =[]

        for att_obj_cl in query_for_marks:
            marks.append(att_obj_cl.attainment)

        marks = mean(marks)

        obj, created = AttainmentPL.objects.update_or_create(program=program_needed, po_id=po,
                                                                year=year_needed,
                                                                defaults={'attainment':marks})
def attainment_course_display(request):
    rk = AttainmentCL.objects.values('co_id__course','year').distinct()

    max_course_outcomes = 0
    all_course_details =[] # course ,year, marks

    for obj in rk: # obj = {'co_id__course:course_id, 'year':year}
        course_id = obj['co_id__course']
        year = obj['year']
        details_of_a_course = [Course.objects.get(id=course_id).name,year]
        cond_1 = Q(co_id__course_id=course_id)
        cond_2 = Q(year=year)
        query_for_marks = AttainmentCL.objects.filter(cond_1 & cond_2)
        total_marks_for_a_course = query_for_marks.aggregate(s=Sum('attainment'))['s']
        total_outcomes_of_a_course = CourseOutcome.objects.filter(course_id=course_id)
        total_outcomes = total_outcomes_of_a_course.count()
        if total_outcomes > max_course_outcomes:
            max_course_outcomes = total_outcomes
        details_of_a_course.append(round(float(total_marks_for_a_course)*100 / total_outcomes,2))
        for mark in total_outcomes_of_a_course:
            try:
                my_match = AttainmentCL.objects.get(co_id=mark)
                details_of_a_course.append(round(my_match.attainment*100,2))
            except AttainmentCL.DoesNotExist:
                details_of_a_course.append(0)
        all_course_details.append(details_of_a_course)
    return render(request, 'assessment/attainment_cl.html', {'details':all_course_details,
                                                             'count':range(1,max_course_outcomes+1),
                                                             })


def attainment_program_display(request):
    rk = AttainmentPL.objects.values('po_id__program', 'year').distinct()
    max_program_outcomes = 15
    all_program_details = []
    for obj in rk:
        program_id = obj['po_id__program']
        year = obj['year']
        details_of_a_program = [Program.objects.get(id=program_id).name, year]
        cond_1 = Q(po_id__program_id=program_id)
        cond_2 = Q(year=year)
        query_for_marks = AttainmentPL.objects.filter(cond_1 & cond_2)
        total_marks_for_a_program = query_for_marks.aggregate(s=Sum('attainment'))['s']
        total_outcomes_of_a_program = ProgramOutcome.objects.filter(program_id=program_id)


        details_of_a_program.append(round(float(total_marks_for_a_program)*100 / 15,2))
        for mark in total_outcomes_of_a_program:
            try:
                my_match = AttainmentPL.objects.get(po_id=mark)
                details_of_a_program.append(round(my_match.attainment*100,2))
            except AttainmentCL.DoesNotExist:
                details_of_a_program.append(0)
        all_program_details.append(details_of_a_program)
    return render(request, 'assessment/attainment_pl.html', {'details':all_program_details,
                                                             'count':range(1,max_program_outcomes+1),
                                                             })