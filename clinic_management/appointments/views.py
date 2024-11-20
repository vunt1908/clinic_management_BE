from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Appointment
from appointments.serializers import AppointmentSerializer
from medicalrecords.serializers import MedicalRecordSerializer

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # return Appointment.objects.all()
    
        user = self.request.user
        if user.role == "patient":
            return Appointment.objects.filter(patient__user=user)
        return Appointment.objects.all()

    def create(self, request, *args, **kwargs):
        patient = request.user.patient
        data = request.data
        data['patient'] = patient.id  

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({
                'status': 'error',
                'errors': serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                'status': 'success',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED, headers=headers)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        appointment = self.get_object()

        status = request.data.get('status')
        if status not in ['pending', 'confirmed', 'completed', 'cancelled']:
            return Response({"detail": "Trạng thái không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

        appointment.status = status
        appointment.save()

        serializer = AppointmentSerializer(appointment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def update_medical_record(self, request, pk=None):
        appointment = self.get_object()
        serializer = MedicalRecordSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(appointment=appointment)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
