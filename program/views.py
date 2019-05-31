from django.shortcuts import render, render_to_response, redirect, reverse, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse_lazy
from .models import Program
from django.views import generic
from .forms import Course_Outcome_Form
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin


@permission_required('program.can_view_program', login_url="denied")
class IndexView(generic.ListView):
    template_name = 'program/index.html'

    def get_queryset(self):
        return Program.objects.all()


@permission_required('course.can_create_program', login_url="denied")
def New_CO(request):
    if request.method == "POST":
        co_form = Course_Outcome_Form(request.POST)
        if co_form.is_valid():
            co_form.save()
            return redirect('program:co-new')
    else:
        co_form = Course_Outcome_Form

    context = {"co_form": co_form,}
    return render(request, 'program/../course/templates/course/co_form.html', context)
