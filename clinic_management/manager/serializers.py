from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Manager
from accounts.models import User

class ManagerSerializer(serializers.ModelSerializer):  
    user = UserSerializer()

    class Meta:
        model = Manager 
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'manager'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        manager = Manager.objects.create(user=user, **validated_data)
        return manager

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