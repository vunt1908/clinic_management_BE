from rest_framework import viewsets
from rest_framework.decorators import action
from datetime import datetime
from patient.models import Patient
from doctor.models import Doctor
from appointments.models import Appointment
from payments.models import Payment
from accounts.views import IsManagerUser
from rest_framework.response import Response
from django.db.models import Count

# Create your views here.
class ManagerDashboardViewSet(viewsets.ViewSet):  
    # permission_classes = [IsManagerUser] 

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        today = datetime.now().date()
        
        stats = {
            'total_patients': Patient.objects.count(),
            'total_doctors': Doctor.objects.count(),
            'total_appointments': Appointment.objects.count(),
            'today_appointments': Appointment.objects.filter(date=today).count(),
            'completed_appointments': Appointment.objects.filter(status='completed').count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'appointments_by_department': Doctor.objects.annotate(
                appointment_count=Count('appointment')
            ).values('department', 'appointment_count')
        }
        
        return Response(stats)