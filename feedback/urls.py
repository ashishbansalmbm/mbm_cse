from django.urls import path
from . import views

app_name='feedback'

urlpatterns = [

     path('', views.IndexView.as_view(), name='index'),
     path('add/<int:coursefeedback_id>/', views.add_ques, name='fb-add'),
     path('new/',views.New_FB, name='fb-new'),
     path('<int:pk>', views.DetailView.as_view(), name='detail'),
     path('<int:pk>/delete/',views.del_ques ,name='ques-delete'),
     path('<int:pk>/update-order/',views.update_ques_order ,name='ques-order-update'),
     path('view/<int:coursefeedback_id>/', views.fill_form, name='view-fb'),
     path('<int:pk>/edit/',views.edit_ques ,name='ques-edit'),
    #path('create/add/', views.add_ques, name='fb-add-ques'),
    #path('add/', views.Create_FB, name='fb-add'),
]
