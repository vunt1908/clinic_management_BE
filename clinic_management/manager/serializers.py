from rest_framework import serializers
from accounts.serializers import UserSerializer
from .models import Manager
from accounts.models import User

class ManagerSerializer(serializers.ModelSerializer):  # Changed from AdminSerializer
    user = UserSerializer()

    class Meta:
        model = Manager  # Changed from Admin
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'manager'  # Changed from admin
        user = User.objects.create(**user_data)
        manager = Manager.objects.create(user=user, **validated_data)  # Changed from Admin
        return manager

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user = instance.user
        
        for attr, value in user_data.items():
            setattr(user, attr, value)
        user.save()
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance