from django.forms import ModelForm, forms
from django import forms
from .models import AssessmentResult, AssessmentQuestion, Assessment
from django.forms.models import modelformset_factory, inlineformset_factory
from student.models import Semester
from program.models import Program
from django.contrib.admin.widgets import AdminDateWidget
from django.forms.fields import DateField
from course.models import Course

class ResultFacultyForm(forms.Form):
    program = forms.CharField(max_length=10)
    semester = forms.ChoiceField(choices=[(tag.name, tag.value) for tag in Semester])
    year = forms.IntegerField()


class ResultForm(forms.Form):
    class Meta:
        model = AssessmentResult

    def __init__(self, *args, **kwargs):
        pack = kwargs.pop('pack')
        super(ResultForm, self).__init__(*args, **kwargs)

        for i, q in pack:
            print('obtained_marks'+str(i)+str(q))
            self.fields['obtained_marks'+str(i)+str(q)] = forms.IntegerField(required=False)


class QuestionForm(ModelForm):
    class Meta:
        model = AssessmentQuestion
        fields = ['question_type', 'text', 'max_marks', 'question_order', 'marking_scheme', 'outcome']


class AssessmentForm(ModelForm):
    class Meta:
        model = Assessment
        fields = ['course', 'assessment_type', 'start_date', 'duration', 'faculty', 'year']
        widgets = {'start_date' :forms.DateInput(attrs={'class': 'datepicker'})}


class Calculate(forms.Form):
    course = forms.ModelChoiceField(queryset=Course.objects.all(), empty_label=None)
    year = forms.ChoiceField()