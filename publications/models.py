from django.db import models
from user.models import User


class Publication(models.Model):
    title = models.CharField(max_length=250)
    publisher_name = models.ForeignKey(User, on_delete=None)
    editorial_name = models.CharField(max_length=100)
    year = models.DateField()
    volume = models.PositiveSmallIntegerField()
    edition = models.PositiveSmallIntegerField()
    pages = models.IntegerField()
    date_of_addition = models.DateTimeField()
    abstract = models.TextField()


class PublicationAuthor(models.Model):
    publication = models.ForeignKey(Publication, on_delete=None)
    author = models.ForeignKey(User, on_delete=None)


class NewsletterSubmission(models.Model):
    author = models.ForeignKey(User, on_delete=None)
    text = models.TextField()
    attachment = models.FileField()
    date = models.DateTimeField()
    edition = models.PositiveSmallIntegerField()


class NewsletterPublished(models.Model):
    editor = models.ForeignKey(User, on_delete=None)
    edition = models.PositiveSmallIntegerField()
    date = models.DateTimeField()
    attachment = models.FileField()
    text = models.TextField()


