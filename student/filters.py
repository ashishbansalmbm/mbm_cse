import django_filters
from .models import Student


class StudentFilter(django_filters.FilterSet):
    user__first_name = django_filters.CharFilter(label="First Name", lookup_expr='icontains')
    user__last_name = django_filters.CharFilter(label="Last Name", lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['user__first_name', 'user__last_name', 'semester', 'program']