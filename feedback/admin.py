from django.contrib import admin
from .models import FeedbackQuestion, FeedbackAnswer

admin.site.register(FeedbackQuestion)
admin.site.register(FeedbackAnswer)