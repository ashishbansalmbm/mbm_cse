from django.urls import path
from . import views

app_name = 'user'
urlpatterns = [
    path('home/', views.home, name='home'),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('register/', views.register, name='register'),
    path('profile/',  views.view_profile, name='view_profile'),
    path('profile/update/', views.update_profile, name='update_profile'),
    path('profile/list/', views.index_view, name='index_view')
]