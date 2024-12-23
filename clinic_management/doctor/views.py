from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from doctor.serializers import DoctorSerializer
from doctor.models import Doctor

class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Doctor created successfully',
            'data': DoctorSerializer(doctor).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        doctor = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Doctor updated successfully',
            'data': DoctorSerializer(doctor).data
        })

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user = instance.user
        
        try:
            with transaction.atomic():
                instance.delete()
                user.delete()
            return Response({
                'status': 'success',
                'message': 'Doctor deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Doctor.objects.all()
        
        department_id = self.request.query_params.get('department', None)
        if department_id:
            queryset = queryset.filter(department_id=department_id)
            
        return queryset
