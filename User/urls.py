from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [

    path('create/', views.UserCreate.as_view(), name='create'),
    path('list/', views.UserList.as_view(), name='user_list'),
    path('list/profile/',  views.UserProfile.as_view(), name='user_profile'),
]
