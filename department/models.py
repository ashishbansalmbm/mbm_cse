from django.db import models


# Create your models here.
class Department(models.Model):
    name = models.CharField(max_length=50)
    head_name = models.CharField(max_length=50)
    foundation_year = models.CharField(max_length=4)
    vision = models.TextField()
    mission = models.TextField()
    resources = models.TextField()
    rules_reg = models.TextField()
    calendar = models.IntegerField()

    def __str__(self):
        return self.name
