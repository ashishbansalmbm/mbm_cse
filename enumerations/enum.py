# all enums
from enum import Enum


class QuestionType(Enum):
    T = "Theory"
    P = "Practical"


class AssessmentType(Enum):
    Int = "Internal"
    M = "Main"


class CourseType(Enum):
    M_TH  = "Mandatory Theory"
    M_LAB = "Mandatory Lab"
    ELEC_TH = "Elective Theory"
    ELEC_LAB = "Elective lab"
    VOL = "Voluntary"


class FeedbackQuestionType(Enum):
    TF = 'True/False'
    MCQ = 'Multiple Choice'
    R = 'Rating'


class FeedbackType(Enum):
    PROG = 'Program'
    CRSE = 'Course'
    PLACE = 'Placement'
    EVNT = 'Event'
    OT = 'Other'

class Semester(Enum):
    SEM_1 = '1st Semester'
    SEM_2 = '2nd Semester'
    SEM_3 = '3rd Semester'
    SEM_4 = '4th Semester'
    SEM_5 = '5th Semester'
    SEM_6 = '6th Semester'
    SEM_7 = '7th Semester'
    SEM_8 = '8th Semester'


class Designation(Enum):
    AST_PROF = "Assistant Professor"
    ASC_PROF = "Associate Professor"
    PROF = "Professor"
    OT = "Other"
