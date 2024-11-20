from rest_framework import serializers
from django.contrib.auth import get_user_model
from accounts.serializers import UserSerializer
from patient.models import Patient
from accounts.models import User
from django.contrib.auth.hashers import make_password


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        password = user_data.pop('password', None)  
        user_data['role'] = 'patient'

        user = User(**user_data)
        if password:
            user.set_password(password) 
        user.save()

        patient = Patient.objects.create(user=user, **validated_data)
        return patient

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user

        password = user_data.pop('password', None)  
        for attr, value in user_data.items():
            setattr(user, attr, value)
        if password:
            user.set_password(password)  
        user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance
    
class RegisterPatientSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    phone = serializers.CharField()
    dob = serializers.DateField()
    address = serializers.CharField()

    def create(self, validated_data):
        user_data = {
            'username': validated_data['username'],
            'email': validated_data['email'],
            'first_name': validated_data['first_name'],
            'last_name': validated_data['last_name'],
            'phone': validated_data['phone'],
            'dob': validated_data['dob'],
            'address': validated_data['address'],
            'password': validated_data['password'],  
            'role': 'patient' 
        }
        
        user = get_user_model().objects.create_user(**user_data)
        patient = Patient.objects.create(user=user)
        
        return patient