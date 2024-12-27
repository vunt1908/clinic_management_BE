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
        """
        Thêm thông tin khám bệnh cho lịch hẹn.
        """
        try:
            appointment = Appointment.objects.get(pk=pk)
            
            # Kiểm tra nếu lịch hẹn đã có thông tin khám bệnh
            if hasattr(appointment, 'examination'):
                return Response({"error": "Lịch hẹn đã có thông tin khám bệnh."}, status=status.HTTP_400_BAD_REQUEST)

            # Tạo mới Examination
            serializer = ExaminationSerializer(data=request.data)
            if serializer.is_valid():
                # Gán lịch hẹn vào examination
                serializer.save(appointment=appointment)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response({"error": "Không tìm thấy lịch hẹn."}, status=status.HTTP_404_NOT_FOUND)
        
    @action(detail=True, methods=["patch"])
    def update_examination(self, request, pk=None):
        """
        Cập nhật thông tin khám bệnh cho lịch hẹn.
        """
        try:
            appointment = Appointment.objects.get(pk=pk)
            # Lấy đối tượng Examination đã có liên kết với lịch hẹn
            examination = appointment.examination
            
            # Sử dụng serializer để cập nhật thông tin examination
            serializer = ExaminationSerializer(examination, data=request.data, partial=True)  # partial=True để chỉ cập nhật phần cần thiết
            if serializer.is_valid():
                serializer.save()  # Lưu lại dữ liệu đã cập nhật
                return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Appointment.DoesNotExist:
            return Response({"error": "Không tìm thấy lịch hẹn."}, status=status.HTTP_404_NOT_FOUND)
        except Examination.DoesNotExist:
            return Response({"error": "Không tìm thấy thông tin khám bệnh cho lịch hẹn này."}, status=status.HTTP_404_NOT_FOUND)