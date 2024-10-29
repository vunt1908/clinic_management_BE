from django.db import models
from django.contrib.auth.models import AbstractUser
from departments.models import Department

# Create your models here.
class User(AbstractUser):
    USER_ROLE_CHOICES = (
        (1, 'Admin'),
        (2, 'Staff'),
        (3, 'Doctor'),
        (4, 'Patient'),
    )
    role = models.PositiveSmallIntegerField(choices=USER_ROLE_CHOICES, default=4)
    email = models.EmailField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.first_name + " " + self.last_name

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor')
    expertise = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

class Staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff')

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name
