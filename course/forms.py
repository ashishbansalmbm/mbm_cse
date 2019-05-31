from django.forms import ModelForm
from . models import Course, CourseAvailable, CourseProgram, CourseEnrollment


class CourseProg_Form(ModelForm):
    class Meta:
        model = CourseProgram
        fields = ['program']


class CourseOffer_Form(ModelForm):
    class Meta:
        model = CourseAvailable
        fields = ['course', 'year']


class Course_Form(ModelForm):
    class Meta:
        model = Course
        fields = ['semester' ,'name','course_code','course_type','max_marks','credits','objective','syllabus',
                  'text_books','ref_material','prerequisite','duration','hours']


class Enroll_Form(ModelForm):
    class Meta:
        model = CourseEnrollment
        fields = ['course']