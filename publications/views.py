from django.contrib.auth.decorators import permission_required, PermissionDenied
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.utils.decorators import method_decorator
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.shortcuts import render, redirect
from .models import Publication, NewsletterPublished, NewsletterSubmission
from django.contrib import messages
from django.db.models import Q
from user.models import User


class IndexUserView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'publications.can_view_publication'
    login_url = "denied"
    template_name = 'publications/index_user.html'

    def get_queryset(self):
        return Publication.objects.all().order_by('-date_of_addition')


class IndexView(generic.ListView):
    template_name = 'publications/index.html'

    def get_queryset(self):
        return Publication.objects.all().order_by('-date_of_addition')


class DetailView(PermissionRequiredMixin, generic.DetailView):
    permission_required = 'publications.can_view_publication'
    model = Publication
    template_name = 'publications/detail.html'


class PublicationCreate(PermissionRequiredMixin, CreateView):
    permission_required = 'publications.add_publication'
    login_url = "denied"
    model = Publication
    template_name = 'publications/publication_form.html'
    fields = ['title', 'type', 'publisher_name', 'editorial_name', 'year',
              'volume', 'doi', 'isbn', 'description', 'edition', 'pages', 'language', 'abstract']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PublicationUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'publications.can_change_publication'
    model = Publication
    fields = ['title', 'type', 'publisher_name', 'editorial_name', 'year',
              'volume', 'doi', 'description', 'edition',
              'pages', 'language', 'abstract']


class PublicationDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'publications.can_delete_publication'
    model = Publication
    success_url = reverse_lazy('publications:index_user')


@permission_required('publications.can_view_publication', raise_exception=PermissionDenied)
def search(request):
    if request.method == 'POST':
        srch = request.POST['srh']

        if srch:
            match = Publication.objects.filter(Q(title__icontains=srch) |
                                               Q(year__icontains=srch) |
                                               Q(type__icontains=srch))
            if match:
                return render(request, 'publications/search.html', {'sr': match})
            else:
                messages.error(request, 'no result found')
        else:
            return redirect(reverse('publications:index_user'))
    return render(request, 'publications/search.html')


class MyPublication(PermissionRequiredMixin, generic.ListView):
    permission_required = 'publications.can_view_publication'
    model = Publication
    template_name = 'publications/my_publication.html'

    def get_queryset(self):
        return Publication.objects.filter(author=self.request.user)


class Index2UserView(generic.ListView):
        template_name = 'publications/index2_user.html'

        def get_queryset(self):
            return NewsletterPublished.objects.all().order_by('-date')


class Index2View(generic.ListView):
            template_name = 'publications/index2.html'

            def get_queryset(self):
                return NewsletterPublished.objects.all().order_by('-date')


class NewsletterSubmissionCreate(PermissionRequiredMixin,CreateView):
    permission_required = 'publications.add_newslettersubmission'
    login_url = 'denied'
    model = NewsletterSubmission
    template_name = 'publications/newsletter_form.html'
    fields = ['title', 'edition', 'description', 'attachment']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class NewsletterDelete(PermissionRequiredMixin, DeleteView):
    permission_required = 'publications.can_delete_newsletter_submission'
    model = NewsletterSubmission
    success_url = reverse_lazy('publications:index2_user')


class NewsletterUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = 'publications.can_change_newsletter_submission'
    model = NewsletterSubmission
    template_name = 'publications/newsletter_form.html'
    fields = ['title', 'edition', 'attachment']


class MySubmission(PermissionRequiredMixin, generic.ListView):
    permission_required = 'publications.can_view_newsletter_submission'
    model = NewsletterSubmission
    template_name = 'publications/my_submission.html'

    def get_queryset(self):
        return NewsletterSubmission.objects.filter(author=self.request.user)


class NewsletterPublish(PermissionRequiredMixin, CreateView):
    permission_required = 'publications.can_add_newsletter_published_editor'
    model = NewsletterPublished
    template_name = 'publications/newsletter_publish_form.html'
    fields = ['title', 'edition', 'text', 'attachment']

    def form_valid(self, form):
        form.instance.editor = self.request.user
        return super().form_valid(form)
    success_url = reverse_lazy('publications:index2_user')


class Index3View(PermissionRequiredMixin, generic.ListView):
    permission_required = 'publications.can_view_newsletter_published_editor'
    template_name = 'publications/index3.html'

    def get_queryset(self):
        return NewsletterSubmission.objects.all().order_by('-date')