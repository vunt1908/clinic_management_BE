from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
        ('nurse', 'Nurse'),
        ('manager', 'Manager'), 
    )

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    phone = models.CharField(max_length=15, null=True)
    dob = models.DateField(null=True)
    address = models.TextField(null=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)