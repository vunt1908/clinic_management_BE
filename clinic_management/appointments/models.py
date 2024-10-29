from django.db import models
from accounts.models import Patient, Doctor, Department

# Create your models here.
class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    start_time = models.TimeField()
    end_time = models.TimeField()
    appointment_date = models.DateField()
    STATUS_CHOICES = (
        ('PENDING', 'pending'),
        ('CONFIRMED', 'confirmed'),
        ('REJECTED', 'rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reasons = models.TextField()
    notes = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
