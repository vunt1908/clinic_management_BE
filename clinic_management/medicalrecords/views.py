from rest_framework import viewsets
from .models import MedicalRecord
from .serializers import MedicalRecordSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

class MedicalRecordViewSet(viewsets.ModelViewSet):
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer

    def get_queryset(self):
        user = self.request.user
        # if hasattr(user, 'doctor'):
        #     return self.queryset.filter(doctor__user=user)
        # elif hasattr(user, 'patient'):
        #     return self.queryset.filter(patient__user=user)
        # return self.queryset.all()
        if hasattr(user, 'patient'):
            return self.queryset.filter(patient__user=user)
        return self.queryset.all()