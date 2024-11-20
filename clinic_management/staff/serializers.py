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
        user = User.objects.create(**user_data)
        staff = Staff.objects.create(user=user, **validated_data)
        return staff

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