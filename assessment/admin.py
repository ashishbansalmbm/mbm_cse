from django.contrib import admin
from .models import Assessment, AssessmentQuestion, AssessmentResult


admin.site.register(Assessment)
admin.site.register(AssessmentQuestion)
admin.site.register(AssessmentResult)