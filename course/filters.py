import django_filters
from .models import CourseProgram


class CourseFilter(django_filters.FilterSet):
    class Meta:
        model = CourseProgram
        fields = ['course__semester', 'course__name', 'program__name']