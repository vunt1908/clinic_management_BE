from rest_framework import serializers
from .models import Department
from accounts.serializers import DoctorSerializer

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ['id', 'name', 'description']