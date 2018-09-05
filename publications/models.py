from django.db import models
from user.models import User
from django.urls import reverse
from datetime import datetime
from enumerations.enum import LanguageChoice, TypeChoice
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import Permission


YEAR_CHOICES = []
for r in range(1900, (datetime.now().year+1)):
    YEAR_CHOICES.append((r, r))


class Publication(models.Model):
    title = models.CharField(max_length=250)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    author1 = models.CharField(max_length=30, null=True)
    publisher_name = models.CharField(max_length=19, blank=True)
    editorial_name = models.CharField(max_length=30, blank=True)
    year = models.IntegerField('year', choices=YEAR_CHOICES, default=datetime.now().year)
    volume = models.PositiveSmallIntegerField()
    doi = models.CharField(max_length=128, verbose_name='DOI', blank=True)
    isbn = models.CharField(max_length=32, verbose_name="ISBN", null=True,
                            help_text='13 character  '
                                      '<a href="https://www.isbn-international.org/content/what-isbn" target="_blank" style="font-size:20px;">'
                                      'What is ISBN?'
                                      '</a>')
    description = models.TextField()
    edition = models.FloatField()
    language = models.CharField(max_length=10,  choices=[(tag.name, tag.value)
                                                         for tag in LanguageChoice], default=LanguageChoice.ENGLISH)
    pages = models.IntegerField(null=True)
    date_of_addition = models.DateField(default=datetime.now())
    abstract = models.TextField()
    type = models.CharField(max_length=30,  choices=[(tag.name, tag.value)
                                                     for tag in TypeChoice], default=TypeChoice.JOURNAL)

    def __str__(self):
        return self.publisher_name + ',' + self.editorial_name + ',' + self.title

    def get_absolute_url(self):
        return reverse('publications:index_user')

    class Meta:
        permissions = {
            ('can_view_publication', 'can view publication'),
        }


class PublicationAuthor(models.Model):
    publication_id = models.ForeignKey(Publication, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=None)


class NewsletterSubmission(models.Model):
    title = models.CharField(max_length=250, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    attachment = models.FileField(upload_to='foo/',
                                  validators=[FileExtensionValidator(allowed_extensions=   ['pdf', 'video/x-msvideo', 'application/pdf', 'video/mp4', 'audio/mpeg', 'docx'])])
    date = models.DateField(default=datetime.now())
    description = models.TextField(max_length=300, null=True)
    edition = models.PositiveSmallIntegerField()

    def get_absolute_url(self):
        return reverse('publications:index2_user')

    def __str__(self):
        return self.title

    class Meta:
        permissions = {
            ('can_view_newsletter_submission', 'can view newsletter submission'),
            ('can_view_newsletter_submission_editor', 'can view newsletter submission editor'),
        }


class NewsletterPublished(models.Model):
    title = models.CharField(max_length=250, blank=True)
    editor = models.ForeignKey(User, on_delete=None)
    text = models.TextField(max_length=300, null=True)
    edition = models.PositiveSmallIntegerField()
    date = models.DateField(default=datetime.now())
    attachment = models.FileField(upload_to='foo/',
                                  validators=[FileExtensionValidator(allowed_extensions=['pdf', 'video/x-msvideo', 'application/pdf', 'video/mp4', 'audio/mpeg', 'docx', 'jpg'])])

    def get_absolute_url(self):
        return reverse('publications:index2_user')

    def __str__(self):
        return self.title



