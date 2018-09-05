from .models import Assessment, Course, Faculty,AssessmentQuestion
import django_filters
class UserFilter(django_filters.FilterSet):
    class Meta:
        model = Assessment
        fields = ['course', 'year']


