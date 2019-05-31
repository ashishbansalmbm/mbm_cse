import django_filters
from .models import Message
from django.contrib.auth.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['username', 'first_name']


class MessageFormFilter(django_filters.FilterSet):

    class Meta:
        model = Message
        fields = ['receiver']