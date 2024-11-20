from rest_framework import viewsets, status
from rest_framework.response import Response
from doctor.serializers import DoctorSerializer
from doctor.models import Doctor
from accounts.views import IsManagerUser

# Create your views here.
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer
    # permission_classes = [IsManagerUser]

    def perform_destroy(self, instance):
        instance.user.delete() 
        instance.delete()

