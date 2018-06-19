from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.UserCreate.as_view(), name='create')
]