from django.db import models


# Create your models here.
class Department(models.Model):
    dept_id = models.CharField(primary_key=True, unique=True, max_length=30)
    name = models.CharField(max_length=50)
    head_name = models.CharField(max_length=50)
    foundation_year = models.CharField(max_length=4)
    vision = models.TextField()
    mission = models.TextField()
    resources = models.TextField()
    rules_reg = models.TextField()
    calendar = models.FileField() # calendar app bookmark

