from django.db import models
from accounts.models import Patient, Doctor

# Create your models here.
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    symptoms = models.TextField() # triệu chứng
    diagnoses = models.TextField() # chẩn đoán
    test_results = models.TextField() # kết quả xét nghiệm
    price = models.DecimalField(max_digits=10, decimal_places=3) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)