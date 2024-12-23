from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Doctor
from accounts.models import User

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department_name = serializers.CharField(source = 'department.name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user','doctor_image', 'expertise', 'department', 'department_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'doctor'

        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', None)
        
        if user_data:
            user_serializer = UserSerializer(
                instance.user,
                data=user_data,
                partial=True
            )
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        
        return instance