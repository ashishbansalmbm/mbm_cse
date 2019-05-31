from django.conf.urls import url
from assessment import views

app_name = 'assessment'

urlpatterns = [


    url(r'^(?P<pk>[0-9]+)/$', views.detail, name='detail'),
    url(r'^(?P<pk>[0-9]+)/detail$', views.assess_detail, name='assess_detail'),
    url(r'^assessment/update/(?P<pk>[0-9]+)/$', views.AssessmentUpdate.as_view(), name='update'),
    url(r'^assessmentQuestion/update/(?P<pk>[0-9]+)/$', views.questionupdate, name='questionupdate'),
    url(r'^result/update/(?P<ass_id>[0-9]+)/$', views.updateresult, name='resultupdate'),
    url(r'^assessment/entry/$', views.createassessment, name='assessment-entry'),
    url(r'^$', views.search, name='index'),
    url(r'^question/entry/(?P<assessment_id>[0-9]+)/$', views.createquestion, name='assessmentquestion-entry'),
    url(r'^self/$', views.student_result_semesterwise, name='selfresult'),
    url(r'^self/(?P<sem>[\w\-]+)/(?P<year>[0-9]+)/$', views.student_result_coursewise, name='selfcourseresult'),
    url(r'^self/course/(?P<pk>[0-9]+)/(?P<year>[0-9]+)/$', views.student_result_assessmentwise, name='selfassessment'),
    url(r'^self/course/question/(?P<pk>[0-9]+)/$', views.student_result_questionwise, name='questionresult'),
    url(r'^result_fac/$',views.faculty_request, name='fac_res'),
    url(r'^result/$',views.result_faculty, name='faculty_result'),
    url(r'^(?P<c_id>[0-9]+)/result_course/$',views.result_course, name='result_course'),
    url(r'^(?P<assess_id>[0-9]+)/result_assessment/$',views.result_assessment, name='result_assessment'),
    url(r'^(?P<stu_id>[0-9]+)/result_student/$',views.result_student, name='result_student'),
    url(r'^getyear/$', views.get_years_for_program, name='get_year'),
    url(r'^attainmentcalres/$', views.attainment_calculate, name= 'attainment-cal'),
    url(r'^letscalculate/$', views.search_or_calculate, name='search_or_calculate'),
    url(r'^attcourse/$', views.attainment_course_display, name='attainment_cl_display'),###
    url(r'^getyears/$', views.get_valid_years, name='attainment_getyears'),
    url(r'^attprogram/$', views.attainment_program_display, name='attainment_pl_display'),
]