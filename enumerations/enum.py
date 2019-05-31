# all enums
from enum import Enum


class QuestionType(Enum):
    Remember = "Remember"
    Understand = "Understand"
    Apply = "Apply"
    Analyze = "Analyze"
    Evaluate = "Evaluate"
    CD = "Create/Design"


class AssessmentType(Enum):
    Int = "Internal"
    M = "Main"


class FeedbackQuestionType(Enum):
    TF = 'True/False'
    MCQ = 'Multiple Choice'
    R = 'Rating'


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


# enum for User_type
class UserType(Enum):
    S = "Student"
    F = "Faculty"
    U = "User"
    A = "Alumni"


# enum for blood group
class BloodGroup(Enum):
    OM = "O-Minus"
    OP = "O-Positive"
    AM = "A-Minus"
    AP = "A-Positive"
    BM = "B-Minus"
    ABM = "AB-Minus"
    ABP = "AB-Positive"
    BP = "B-Positive"


class Gender(Enum):
    M = "Male"
    F = "Female"
    OT = "Other"


class Category(Enum):
    GEN = "General"
    OBC = "Other Backward Class"
    SC = "Scheduled Caste"
    ST = "Scheduled Tribe"


class CourseType(Enum):
    MTH  = "Mandatory Theory"
    MLAB = "Mandatory Lab"
    ELECTH = "Elective Theory"
    ELECLAB = "Elective lab"
    VOL = "Voluntary"


class FeedbackType(Enum):
    PROG = 'Program'
    CRSE = 'Course'
    PLACE = 'Placement'
    EVNT = 'Event'
    OT = 'Other'


class MessageType(Enum):
    M = 'Message'
    N = 'Notice'
    B = 'Broadcast'


class CoPoLink(Enum):
    N = 'None'
    H = 'High'
    S = 'Slight'
    M = 'Minimum'


class LanguageChoice(Enum):
    HINDI = "Hindi"
    ENGLISH = "English"
    GERMAN = "German"


class TypeChoice(Enum):
    JOURNAL = "Journal"
    BOOK = "Book"
    THESIS = "Thesis"
    ResearchPaper = "Research Paper"
    ConferencePaper = "Conference Paper"
    EducationalMaterials = "Educational Materials"
    Talks = "Talks"
    OTHERS = "Others"