from rest_framework import serializers
from .models import Appointment
from patient.serializers import PatientSerializer
from doctor.serializers import DoctorSerializer
from patient.models import Patient
from doctor.models import Doctor

class AppointmentSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer()
    patient = PatientSerializer()
    
    class Meta:
        model = Appointment
        fields = '__all__'
