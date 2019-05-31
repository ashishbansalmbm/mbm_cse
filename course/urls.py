from django.urls import path
from . import views



app_name = 'course'

urlpatterns = [
     path('', views.IndexView, name='index'),
     path('<int:pk>/', views.DetailView , name='detail'),
     path('add/', views.CourseCreate, name='course-add'),
     path('<int:pk>/update/',views.CourseUpdate, name='course-update'),
     path('<int:pk>/delete/',views.CourseDelete, name='course-delete'),
     path('search/', views.search, name='course-search'),
     path('<int:pk>/add-co/', views.Add_CO, name='co-new'),
     path('<int:co>/select-po/', views.Select_PO, name='po-select'),
     path('availableCourses/', views.OfferCoursesIndex ,name='course-offeredlist'),
     path('offerCourses/', views.OfferCourses, name='course-offer'),
     path('<int:ca_id>/enroll|std/', views.Enroll_Student, name='enroll-student'),
     path('faculty/', views.My_Course_Faculty, name='mycourse-faculty'),
     path('student/', views.My_Course_Student, name='mycourse-student'),
     path('<int:co>/see-links/', views.See_Links , name='see-links'),
     #path('<int:pk>/add-co/', views.Add_CO, name='co-add'),

]
