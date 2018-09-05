from django.contrib import admin
from .models import Publication, NewsletterSubmission, NewsletterPublished
# Register your models here.
admin.site.register(Publication)
admin.site.register(NewsletterSubmission)
admin.site.register(NewsletterPublished)