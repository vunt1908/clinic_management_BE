from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from datetime import datetime, timedelta
from patient.models import Patient
from doctor.models import Doctor
from appointments.models import Appointment
from payments.models import Payment
from accounts.views import IsManagerUser
from rest_framework.response import Response
from django.db.models import Count, Sum
from .models import Manager
from .serializers import ManagerSerializer
from nurse.models import Nurse
from staff.models import Staff
from services.models import Services
from services.serializers import ServicesSerializer

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all()
    serializer_class = ManagerSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        manager = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Thêm mới quản lý thành công.',
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
            'message': 'Cập nhật thông tin quản lý thành công.',
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
                'message': 'Xoá thành công quản lý.'
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
        current_month = today.replace(day=1)
        current_year = today.replace(month=1, day=1)
        filter_type = request.GET.get('filter', 'week')
        data = []

        if filter_type == "week":
            start_of_week = today - timedelta(days=today.weekday())
            for i in range(7):
                day = start_of_week + timedelta(days=i)
                total = Payment.objects.filter(updated_at__date=day, status='completed').aggregate(total=Sum('amount'))['total'] or 0
                data.append({"label": day.strftime("%A"), "value": total})
        elif filter_type == "month":
            for month in range(1, 13):
                total = Payment.objects.filter(
                    updated_at__month=month, updated_at__year=today.year, status='completed'
                ).aggregate(total=Sum('amount'))['total'] or 0
                data.append({"label": f"Tháng {month}", "value": total})

        stats = {
            'total_patients': Patient.objects.count(),
            'total_doctors': Doctor.objects.count(),
            'total_nurses': Nurse.objects.count(),
            'total_staffs': Staff.objects.count(),
            'total_appointments': Appointment.objects.count(),
            'completed_appointments': Appointment.objects.filter(status='completed').count(),
            'upcoming_appointments': Appointment.objects.filter(date__gte=today).exclude(status='completed').count(),
            'today_appointments': Appointment.objects.filter(date=today).count(),
            'month_appointments': Appointment.objects.filter(date__gte=current_month).count(),
            'pending_payments': Payment.objects.filter(status='pending').count(),
            'completed_payments': Payment.objects.filter(status='completed').count(),
            'total_payments': Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0,
            'today_payments': Payment.objects.filter(created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0,
            'total_services': Services.objects.count(),
            "chart_data": data,
        }

        most_selected_service = Services.objects.annotate(
            num_examinations=Count('examinations')
        ).order_by('-num_examinations').first()

        if most_selected_service:
            most_selected_service_data = ServicesSerializer(most_selected_service).data
            stats['most_selected_service'] = most_selected_service_data
        else:
            stats['most_selected_service'] = None

        return Response(stats)