from django.db import models
from .models import Patient, Doctor, Staff, Department
from django.utils import timezone

# Create your models here.
# class Reception(models.Model):
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     department = models.ForeignKey(Department, on_delete=models.CASCADE)
#     reason = models.TextField()
#     reception_time = models.DateField(default=timezone.now())
    
#     def __str__(self):
#         return self.patient
    
# class Waiting(models.Model):
#     doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
#     patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
#     added_at = models.DateTimeField(auto_now_add=True)