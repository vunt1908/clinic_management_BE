from django.db import models
from services.models import Services
from payments.models import Payment
from appointments.models import Appointment

class Examination(models.Model):
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name="examination"
    )
    services = models.ManyToManyField(
        Services,
        related_name="examinations",
        null=True,
        blank=True
    )
    payment = models.OneToOneField(
        Payment, 
        on_delete=models.CASCADE, 
        related_name="examination",
        null=True,
        blank=True
    )
    pathological_process = models.TextField()
    personal_history = models.TextField()
    family_history = models.TextField()
    symptoms = models.TextField()
    diagnosis = models.TextField()
    paraclinical_results = models.FileField(upload_to='paraclinical_results/', null=True, blank=True)
    results = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)