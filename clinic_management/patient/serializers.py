from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from patient.models import Patient
from accounts.models import User

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'job']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'patient'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        patient = Patient.objects.create(user=user, **validated_data)
        return patient

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