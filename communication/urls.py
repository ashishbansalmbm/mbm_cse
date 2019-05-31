from django.urls import path
from . import views

app_name = 'communication'

urlpatterns = [
    path('send/', views.send, name='send'),
    path('read/', views.read, name='read'),
    path('read/<int:pk>/', views.read_view, name='read_view'),
    path('block/<int:pk>/', views.block, name='block'),
    path('unblock/<int:pk>/', views.unblock, name='unblock'),
    path('receive/', views.receive, name='receive'),
    path('create/group/',  views.create_group, name='create_group'),
    path('create/notification/',views.notificationCreate,name='create_notification')


]