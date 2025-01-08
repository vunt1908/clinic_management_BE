from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework import viewsets
from .models import Appointment
from appointments.serializers import AppointmentSerializer
from doctor.models import Doctor
from datetime import datetime

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = Appointment.objects.select_related('doctor', 'patient')
        if hasattr(user, 'doctor'):
            return queryset.filter(doctor__user=user)
        elif hasattr(user, 'patient'):
            return queryset.filter(patient__user=user)
        else:
            return queryset.all()

    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        doctor_id = request.query_params.get('doctor')
        date = request.query_params.get('date')

        if not doctor_id or not date:
            return Response({
                'status': 'error',
                'message': 'Vui lòng cung cấp bác sĩ và ngày khám.'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            doctor = Doctor.objects.get(id=doctor_id)

            try:
                datetime.strptime(date, '%Y-%m-%d')  
            except ValueError:
                return Response({
                    'status': 'error',
                    'message': 'Định dạng ngày không hợp lệ. Vui lòng sử dụng định dạng YYYY-MM-DD.'
                }, status=status.HTTP_400_BAD_REQUEST)

            available_slots = Appointment.get_available_slots(doctor_id, date)

            return Response({
                'status': 'success',
                'doctor': {
                    'id': doctor.id,
                    'name': doctor.user.get_full_name()
                },
                'date': date,
                'available_slots': available_slots
            })
        except Doctor.DoesNotExist:
            return Response({
                'status': 'error',
                'message': 'Bác sĩ không tồn tại.'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': f'Lỗi xảy ra: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @action(detail=True, methods=["patch"])
    def update_status(self, request, pk=None):
        try:
            appointment = self.get_object()
            new_status = request.data.get('status')

            if new_status not in [status[0] for status in Appointment.STATUS_CHOICES]:
                return Response({"error": "Trạng thái không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

            appointment.status = new_status
            appointment.save()

            return Response(AppointmentSerializer(appointment).data)

        except Appointment.DoesNotExist:
            return Response({"error": "Lịch hẹn không tồn tại."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['post'])
    def staff_create(self, request):
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status': 'success',
            'message': 'Lịch hẹn được tạo thành công.',
            'appointment': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def staff_list(self, request):
        appointments = Appointment.objects.all().select_related('doctor', 'patient')
        serializer = self.get_serializer(appointments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
        



    