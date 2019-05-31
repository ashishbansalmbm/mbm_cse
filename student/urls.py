from django.urls import path
from . import views

app_name = 'student'
urlpatterns = [
    path('update/', views.update, name='update'),
    path('profile/<int:pk>/', views.profile, name='profile'),
    path('list/', views.show_student_list, name='student_list'),
]