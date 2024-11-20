from django.db import models
from accounts.models import User
from departments.models import Department

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    expertise = models.CharField(max_length=200, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.user.username