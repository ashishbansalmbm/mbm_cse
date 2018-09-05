from django.contrib import admin
from .models import Course, CourseFeedback, CourseOutcome, CoPo, CourseProgram, CourseAvailable, CourseEnrollment


admin.site.register(Course)
admin.site.register(CourseFeedback)
admin.site.register(CourseOutcome)
admin.site.register(CourseProgram)
admin.site.register(CourseAvailable)
admin.site.register(CourseEnrollment)
admin.site.register(CoPo)