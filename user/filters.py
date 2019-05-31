from student.models import Student
import django_filters


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Student
        fields = ['semester']