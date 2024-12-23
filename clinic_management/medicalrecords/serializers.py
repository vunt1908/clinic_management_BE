from rest_framework import serializers
from .models import MedicalRecord
from appointments.models import Appointment

class MedicalRecordSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = '__all__'
