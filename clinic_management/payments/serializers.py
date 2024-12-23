from rest_framework import serializers
from .models import Payment

class PaymentSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    updated_at = serializers.DateTimeField(format='%Y-%m-%d %H:%M:%S', read_only=True)
    class Meta:
        model = Payment
        fields = '__all__'