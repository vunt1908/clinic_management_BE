from django.db import models
from accounts.models import User
from departments.models import Department

# Create your models here.
class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    doctor_image = models.ImageField(upload_to='doctor_images/', null=True, blank=True)
    expertise = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    def __str__(self):
        return self.user.get_full_name()