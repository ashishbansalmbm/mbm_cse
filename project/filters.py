from .models import Project
import django_filters

class IndexFilter(django_filters.FilterSet):
    class Meta:
        model=Project
        fields=['type' ,]