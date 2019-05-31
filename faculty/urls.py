from django.urls import path
from . import views

app_name='faculty'
urlpatterns = [
    path('update/profile/', views.updateFacultyProfile, name='register'),
    path('list/', views.showFacultyList, name='faculty_list'),
    path('student/list/', views.student_list ,name='student_list'),
    path('profile/', views.viewProfileFaculty,name='faculty_profile'),
]