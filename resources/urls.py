from django.urls import path
from . import views

app_name = 'resources'
urlpatterns = [

    path('user/resources', views.IndexUserView.as_view(), name='index_user'),
    path('', views.IndexView.as_view(), name='index'),
    path('resource/add/', views.ResourcesCreate.as_view(), name='resources-add'),
    path('resource/<int:pk>/update/', views.ResourcesUpdate.as_view(), name='resources-update'),
    path('resource/<int:pk>/delete/', views.ResourcesDelete.as_view(), name='resources-delete'),
    path('resource/my_resource/', views.MyResource.as_view(), name='resource-my'),
    path('resource/search/', views.search, name='resource-search'),

]