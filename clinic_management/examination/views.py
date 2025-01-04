from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Examination
from .serializers import ExaminationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from appointments.models import Appointment

class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

    def get_queryset(self):
        user = self.request.user
        appointment_id = self.request.query_params.get('appointment')

        if appointment_id:
            return Examination.objects.filter(appointment_id=appointment_id)

        if hasattr(user, 'patient'): 
            return Examination.objects.filter(appointment__patient=user.patient)
        elif hasattr(user, 'doctor'):
            return Examination.objects.filter(appointment__doctor=user.doctor)
        else:  
            return Examination.objects.all()

    @action(detail=False, methods=["get"])
    def patient_history(self, request):
        if not hasattr(request.user, 'patient'):
            return Response({"error": "Người dùng không phải là bệnh nhân."}, status=403)
        
        queryset = Examination.objects.filter(appointment__patient=request.user.patient)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
    @action(detail=False, methods=["patch"])
    def assign_services(self, request, pk=None):
        try:
            examination = self.get_object()
            services = request.data.get('services', [])
            examination.services.set(services)
            examination.save()
            return Response({"message": "Dịch vụ đã được chỉ định thành công."})
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    @action(detail=True, methods=["post"])
    def add_examination(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            
            if hasattr(appointment, 'examination'):
                return Response({"error": "Lịch hẹn đã có thông tin khám bệnh."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = ExaminationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(appointment=appointment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response({"error": "Không tìm thấy lịch hẹn."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["patch"])
    def update_examination(self, request, pk=None):
        try:
            appointment = Appointment.objects.get(pk=pk)
            examination = appointment.examination
            serializer = ExaminationSerializer(examination, data=request.data, partial=True)  
            if serializer.is_valid():
                serializer.save()  
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response({"error": "Không tìm thấy lịch hẹn."}, status=status.HTTP_404_NOT_FOUND)
        except Examination.DoesNotExist:
            return Response({"error": "Không tìm thấy thông tin khám bệnh cho lịch hẹn này."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["patch"])
    def update_payment_status(self, request, pk=None):
        try:
            examination = self.get_object()  
            payment = examination.payment  

            if not payment:
                return Response({"error": "Không tìm thấy thông tin thanh toán."}, status=status.HTTP_404_NOT_FOUND)

            new_status = request.data.get("status", None) 
            if new_status not in ["pending", "completed", "failed"]:
                return Response({"error": "Trạng thái không hợp lệ."}, status=status.HTTP_400_BAD_REQUEST)

            payment.status = new_status
            payment.save()

            return Response(
                {"message": f"Trạng thái thanh toán đã được cập nhật thành {new_status}."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)