from django.urls import path
from . import views

app_name = 'publications'
urlpatterns = [

    path('user/publication', views.IndexUserView.as_view(), name='index_user'),
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>', views.DetailView.as_view(), name='detail'),
    path('publication/add/', views.PublicationCreate.as_view(), name='publication-add'),
    path('publication/<int:pk>/update/', views.PublicationUpdate.as_view(), name='publication-update'),
    path('publication/<int:pk>/delete/', views.PublicationDelete.as_view(), name='publication-delete'),
    path('publication/search/', views.search, name='publication-search'),
    path('publication/my_publication/', views.MyPublication.as_view(), name='publication-my'),
    path('user/newsletters', views.Index2UserView.as_view(), name='index2_user'),
    path('newsletters/', views.Index2View.as_view(), name='index2'),
    path('newsletters/add/', views.NewsletterSubmissionCreate.as_view(), name='newsletter-add'),
    path('newsletters/<int:pk>/update/', views.NewsletterUpdate.as_view(), name='newsletter-update'),
    path('newsletters/<int:pk>/delete', views.NewsletterDelete.as_view(), name='newsletter-delete'),
    path('newsletters/my_submission/', views.MySubmission.as_view(), name='newsletter-my'),
    path('newsletter-submissions/', views.Index3View.as_view(), name='index3'),
    path('newsletters/publish/', views.NewsletterPublish.as_view(), name='newsletter-publish'),
]