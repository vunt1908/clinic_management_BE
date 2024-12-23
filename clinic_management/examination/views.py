from django.shortcuts import render
from rest_framework import viewsets, status
from .models import Examination
from .serializers import ExaminationSerializer
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.
class ExaminationViewSet(viewsets.ModelViewSet):
    queryset = Examination.objects.all()
    serializer_class = ExaminationSerializer

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'patient'): 
            return Examination.objects.filter(appointment__patient=user.patient)
        else:  
            return Examination.objects.all()

    @action(detail=False, methods=["get"])
    def patient_history(self, request):
        if not hasattr(request.user, 'patient'):
            return Response({"error": "Người dùng không phải là bệnh nhân."}, status=403)
        
        queryset = Examination.objects.filter(appointment__patient=request.user.patient)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=["patch"])
    def update_payment_status(self, request, pk=None):
        try:
            examination = self.get_object()
            payment = examination.payment
            if payment.status == "pending":
                payment.status = "completed"
                payment.save()
                return Response({"message": "Cập nhật trạng thái thanh toán thành công."})
            else:
                return Response({"error": "Thanh toán đã hoàn thành hoặc không thể cập nhật."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)