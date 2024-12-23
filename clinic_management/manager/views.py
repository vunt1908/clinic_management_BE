from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from datetime import datetime
from patient.models import Patient
from doctor.models import Doctor
from appointments.models import Appointment
from payments.models import Payment
from accounts.views import IsManagerUser
from rest_framework.response import Response
from django.db.models import Count
from .models import Manager
from .serializers import ManagerSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        manager = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Manager created successfully',
            'data': ManagerSerializer(manager).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Manager updated successfully',
            'data': ManagerSerializer(manager).data
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
                'message': 'Manager deleted successfully'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Manager.objects.all()
        return queryset


class DashboardViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        today = datetime.now().date()

        stats = {
            'total_patients': Patient.objects.count(),
            'total_doctors': Doctor.objects.count(),
            'total_appointments': Appointment.objects.count(),
            'today_appointments': Appointment.objects.filter(date=today).count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'completed_payments': Payment.objects.filter(status='completed').count(),
        }

        return Response(stats)