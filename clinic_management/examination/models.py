from django.db import models
from appointments.models import Appointment
from services.models import Services
from medicalrecords.models import MedicalRecord
from payments.models import Payment

# Create your models here.
class Examination(models.Model):
    appointment = models.OneToOneField(
        Appointment, 
        on_delete=models.CASCADE, 
        related_name="examination"
    )
    services = models.ManyToManyField(
        Services,
        related_name="examinations"
    )
    medical_record = models.OneToOneField(
        MedicalRecord, 
        on_delete=models.CASCADE, 
        related_name="examination"
    )
    payment = models.OneToOneField(
        Payment, 
        on_delete=models.CASCADE, 
        related_name="examination"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)