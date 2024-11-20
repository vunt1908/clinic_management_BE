from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Doctor
from accounts.models import User

class DoctorSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    department_name = serializers.CharField(source = 'department.name', read_only=True)

    class Meta:
        model = Doctor
        fields = ['id', 'user', 'expertise', 'department', 'department_name']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'doctor'
        password = user_data.pop('password', None)
        user = User.objects.create(**user_data)
        if password:
            user.set_password(password) 
            user.save()
        doctor = Doctor.objects.create(user=user, **validated_data)
        return doctor

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