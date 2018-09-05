from django.contrib.auth.models import User
from django.db import models
from enumerations.enum import FeedbackQuestionType, FeedbackType
from user.models import Profile


class FeedbackQuestion(models.Model):
    feedback_type = models.CharField(max_length=10, choices=[(tag.name, tag.value) for tag in FeedbackType],
                                     default=FeedbackType.CRSE)
    feedback = models.BigIntegerField()#coursefeedback.id / Progfeedback.id...
    ques_type = models.CharField(max_length=5, choices=[(tag.name, tag.value) for tag in FeedbackQuestionType],
                                default=FeedbackQuestionType.TF)
    options = models.TextField()
    quesText = models.TextField()
    order = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.quesText


class FeedbackAnswer(models.Model):
    question = models.ForeignKey(FeedbackQuestion, on_delete=None)
    user = models.ForeignKey(User, on_delete=None)
    answer = models.PositiveSmallIntegerField()
