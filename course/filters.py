import django_filters
from django_filters import widgets
from django_filters.widgets import LinkWidget

from program.models import Program
from .models import CourseProgram


class CourseFilter(django_filters.FilterSet):

    program__name = django_filters.ModelChoiceFilter(queryset=Program.objects.all())
    class Meta:
        model = CourseProgram
        fields = ['course__semester', 'course__name', 'program__name']