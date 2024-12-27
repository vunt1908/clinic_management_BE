from rest_framework import serializers
from .models import Examination
from services.models import Services

class ExaminationSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)

    services = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Services.objects.all(),
        required=False
    )

    class Meta:
        model = Examination
        fields = '__all__'
