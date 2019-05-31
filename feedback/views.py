from django.shortcuts import render, render_to_response, redirect, reverse, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy
from user.models import Profile
from .models import FeedbackQuestion, FeedbackAnswer
from course.models import CourseFeedback
from .forms import Feedback_Ques_Form, Course_Feedback_Form, Feedback_Ans_Form
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views import generic

class IndexView(generic.ListView):
    template_name = 'feedback/index.html'
    def get_queryset(self):
        return FeedbackQuestion.objects.all()


class DetailView(generic.DetailView):
        model = FeedbackQuestion
        template_name = 'feedback/detail.html'


def New_FB(request):
    if request.method == "POST":
        course_form = Course_Feedback_Form(request.POST)

        if course_form.is_valid():
            course_fb = course_form.save(commit=False)
            course_fb.created_by = request.user
            course_fb.save()

            return redirect('feedback:fb-add', coursefeedback_id = course_fb.pk)

    else:
        course_form = Course_Feedback_Form()

    context = {"course_form": course_form,}
    return render(request, 'feedback/new_fb.html', context)


def add_ques(request, coursefeedback_id):
    if request.method == "POST":
        course_fbs = FeedbackQuestion.objects.filter(feedback= coursefeedback_id)
        ques_form = Feedback_Ques_Form(request.POST)
        coursefeedback = CourseFeedback.objects.get(pk= coursefeedback_id)
        order = request.POST.get('order')
        quesText = request.POST.get('quesText')
        ques_type = request.POST.get('ques_type')
        options = request.POST.get('options')
        if ques_form.is_valid():
            ques = ques_form.save(False)
            ques.feedback_type = 'CRSE'
            ques.order = order
            ques.quesText = quesText
            ques.ques_type = ques_type
            ques.options = options
            ques.feedback = coursefeedback_id
            ques.save()

            return redirect('feedback:fb-add', coursefeedback_id = coursefeedback_id)
    else:
        ques_form = Feedback_Ques_Form()
        course_fbs = FeedbackQuestion.objects.filter(feedback = coursefeedback_id)
        coursefeedback = CourseFeedback.objects.get(pk = coursefeedback_id)

    context = {'ques_form': ques_form,
               'course_fbs': course_fbs,
               'coursefeedback':coursefeedback, }
    return render(request, 'feedback/feedback_form.html', context)


def del_ques(request, pk):
    instance = FeedbackQuestion.objects.get(pk = pk )
    fb_id = instance.feedback
    instance.delete()
    return redirect('feedback:fb-add', coursefeedback_id=fb_id)


def update_ques_order(request, pk):
    instance = FeedbackQuestion.objects.filter(pk = pk ).update(order=request.GET.get('o'))
    res={}
    res['success']= True
    return JsonResponse(res)


def edit_ques(request, pk):
    instance = get_object_or_404(FeedbackQuestion, pk=pk)
    fb_id = instance.feedback
    if request.method == "POST":
        ques_form = Feedback_Ques_Form(request.POST, instance=instance)
        coursefeedback = CourseFeedback.objects.get(pk=fb_id)
        if ques_form.is_valid():
            ques_form.save()
            return redirect('feedback:fb-add', coursefeedback_id = fb_id)
    else:
        ques_form = Feedback_Ques_Form(instance=instance)
        coursefeedback = CourseFeedback.objects.get(pk=fb_id)
    return render(request, 'feedback/edit_ques.html', {'ques_form': ques_form, 'coursefeedback': coursefeedback,})


def view_form(request, coursefeedback_id):
    coursefeedback = CourseFeedback.objects.get(pk=coursefeedback_id)
    course_fbs = FeedbackQuestion.objects.filter(feedback=coursefeedback_id).order_by('order')
    return render(request, 'feedback/view_form.html', {'coursefeedback': coursefeedback, 'course_fbs': course_fbs, })


def fill_form(request, coursefeedback_id):
    coursefeedback = CourseFeedback.objects.get(pk=coursefeedback_id)
    questions = FeedbackQuestion.objects.filter(feedback=coursefeedback_id).order_by('order')
    if request.method == "POST":
        answers = {}
        a = []
        for q in questions:

            a.append(q.id)
        for q in questions:
            answers[q.id] = request.POST['answer' + str(q.id)]
            form = Feedback_Ans_Form(request.POST or None, a=a)

            if form.is_valid():
                ans = FeedbackAnswer()
                ans.user = request.user
                ans.question = FeedbackQuestion.objects.get(id=q.id)
                ans.answer = answers[q.id]
                ans.save()
            else:
                return HttpResponse('form is not valid')
        return redirect('feedback:index')

    else:
        a = []
        list = []
        for q in questions:
            a.append(q.id)

            if q.ques_type=='MCQ':
                var=q.options.split(',')
                list.append(var)
            else:
                var=[]
                list.append(var)
        print(list)
        form = Feedback_Ans_Form(request.GET or None, a=a)
        abc=zip(questions,list)
    return render(request, 'feedback/fill_form.html', {'form': form,'coursefeedback': coursefeedback,'loop':abc})
