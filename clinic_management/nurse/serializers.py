from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Nurse
from accounts.models import User

class NurseSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Nurse
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'nurse'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        nurse = Nurse.objects.create(user=user, **validated_data)
        return nurse

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