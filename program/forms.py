from django.forms import ModelForm
from course.models import CourseOutcome, CoPo

class Course_Outcome_Form(ModelForm):
    class Meta:
        model = CourseOutcome
        fields = ['text']


class CoPo_Link_Form(ModelForm):
    class Meta:
        model = CoPo
        fields = ['program_outcome', 'level']
