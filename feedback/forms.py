from django.forms import ModelForm, forms
from django import forms
from . models import FeedbackQuestion, FeedbackAnswer
from course.models import CourseFeedback

class Feedback_Ques_Form(ModelForm):
    class Meta:
        model = FeedbackQuestion
        fields = ['order', 'quesText', 'ques_type' , 'options']

class Course_Feedback_Form(ModelForm):
    class Meta:
        model = CourseFeedback
        fields = ['course' , 'year']

class Feedback_Ans_Form(forms.Form):
    class Meta:
        model = FeedbackAnswer

    def __init__(self, *args, **kwargs):
        a = kwargs.pop('a')
        super(Feedback_Ans_Form, self).__init__(*args, **kwargs)

        for i in a:
            print('answer' + str(i))
            self.fields['answer' + str(i)] = forms.IntegerField(required=False)