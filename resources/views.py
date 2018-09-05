from django.contrib.auth.decorators import permission_required, PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import generic, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib import messages
from .models import Resources


class IndexUserView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'resources.can_view_resources'
    template_name = 'resources/index_user.html'

    def get_queryset(self):
        return Resources.objects.all().order_by('-date')


class IndexView(generic.ListView):
    template_name = 'resources/index.html'

    def get_queryset(self):
        return Resources.objects.all().order_by('-date')


class ResourcesCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'resources.can_add_resources'
    model = Resources
    template_name = 'resources/resources_form.html'
    fields = ['title', 'type', 'attachment']

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


@permission_required('resources.can_view_resources', raise_exception=PermissionDenied)
def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match = Resources.objects.filter(Q(title__icontains=srch) |
                                               Q(date__icontains=srch) |
                                               Q(type__icontains=srch))
            if match:
                return render(request, 'resources/search.html', {'sr': match})
            else:
                messages.error(request, 'no result found')
        else:
            return redirect(reverse('resources:index_user'))
    return render(request, 'resources/search.html')



class ResourcesUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'resources.can_change_resources'
    model = Resources
    fields = ['title', 'type', 'attachment'
              ]


class ResourcesDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'resources.can_delete_resources'
    model = Resources
    success_url = reverse_lazy('resources:index_user')


class MyResource(PermissionRequiredMixin, generic.ListView):
    permission_required = 'resources.can_view_resources'
    model = Resources
    template_name = 'resources/my_resource.html'

    def get_queryset(self):
        return Resources.objects.filter(created_by=self.request.user)



