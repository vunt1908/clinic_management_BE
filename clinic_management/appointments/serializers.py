from rest_framework import serializers
from .models import Appointment
from patient.serializers import PatientSerializer
from doctor.serializers import DoctorSerializer
from patient.models import Patient
from doctor.models import Doctor

class AppointmentSerializer(serializers.ModelSerializer):
    # price = serializers.IntegerField(source= 'doctor.examination_price', read_only=True)
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    
    class Meta:
        model = Appointment
        fields = ['id', 'time_slot', 'date', 'notes', 'reason', 'status', 'created_at', 'doctor', 'patient']

