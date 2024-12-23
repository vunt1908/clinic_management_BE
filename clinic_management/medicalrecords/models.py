from django.db import models
from patient.models import Patient
from doctor.models import Doctor
from appointments.models import Appointment

# Create your models here.
class MedicalRecord(models.Model):
    # appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)
    pathological_process = models.TextField(blank=True, null=True)
    personal_history = models.TextField(blank=True, null=True)
    family_history = models.TextField(blank=True, null=True)
    symptoms = models.TextField()
    diagnosis = models.TextField()
    paraclinical_results = models.FileField(upload_to='paraclinical_results/', null=True, blank=True)
    results = models.TextField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)