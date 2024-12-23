from django.db import models
from appointments.models import Appointment
from patient.models import Patient
from services.models import Services

# Create your models here.
class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, blank=True, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
