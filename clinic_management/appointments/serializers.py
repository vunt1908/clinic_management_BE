from rest_framework import serializers
from .models import Appointment

class AppointmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = Appointment
        fields = ['id', 'patient', 'doctor', 'start_time', 'end_time', 'appointment_date', 'status', 'reasons', 'notes', 'price', 'created_at', 'updated_at']
