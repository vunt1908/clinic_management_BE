from django.db import models
from patient.models import Patient
from doctor.models import Doctor
from appointments.models import Appointment

# Create your models here.
class MedicalRecord(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    results = models.TextField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)