from rest_framework import serializers
from .models import Examination
from services.models import Services

class ExaminationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Services.objects.all()
    )

    class Meta:
        model = Examination
        fields = '__all__'

    def create(self, validated_data):
        services_data = validated_data.pop('services', [])
        examination = Examination.objects.create(**validated_data)
        examination.services.set(services_data)  
        return examination

    def update(self, instance, validated_data):
        services_data = validated_data.pop('services', None)
        if services_data is not None:
            instance.services.set(services_data) 
        return super().update(instance, validated_data)
