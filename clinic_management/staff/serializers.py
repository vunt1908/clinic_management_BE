from rest_framework import serializers
from accounts.serializers import UserSerializer
from staff.models import Staff
from accounts.models import User

class StaffSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Staff
        fields = ['id', 'user']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user_data['role'] = 'staff'
        
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()

        staff = Staff.objects.create(user=user, **validated_data)
        return staff

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