from django.db import models
from department.models import Department
from enumerations.enum import Designation

from user.models import User


# Create your models here.

class Faculty(models.Model):
    user = models.OneToOneField(User,on_delete=None)
    department = models.ForeignKey(Department,on_delete=None)
    date_of_join = models.DateField()
    date_of_leave = models.DateField(null=True)
    qualification = models.CharField(max_length=50)
    designation = models.CharField(max_length=10,choices=[(tag.name, tag.value) for tag in Designation])
    specialization = models.CharField(max_length=50)
    description = models.TextField()
    submit = models.BooleanField(default=False)
    # employ_id = models.ForeignKey(Employ, on_delete=None)

    class Meta:
        permissions = (('can_update_profile', 'can update profile'),
                       ('can_view_self_profile', 'can view self profile'),
                       ('can_view_student_list', 'can view student list'),
                       )

    def __str__(self):
        return self.user.get_full_name()



