from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Appointment
from .serializers import AppointmentSerializer

# Create your views here.
# class AppointmentViewSet(viewsets.ViewSet):
#     queryset = Appointment.objects.all()
#     serializer_class = AppointmentSerializer
    
#     def create(self, request):
#         if self.request.user.role != 'patient':
#             return Response({'error': 'Only patients can create appointments'}, status=status.HTTP_403_FORBIDDEN)

#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(patient=request.user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def patial_update(self, request):
#         appointment = self.get_object()
#         if request.user != appointment.doctor:
#             return Response({'error': 'Only doctors can update appointments'}, status=status.HTTP_403_FORBIDDEN)
        
#         status_update = request.data.get('status')
#         if status_update in ['confirmed', 'rejected']:
#             appointment.status = status_update
#             appointment.save()
#             return Response({"message": "Appointment status updated successfully."}, status=status.HTTP_200_OK)
#         return Response({"error": "Invalid status update."}, status=status.HTTP_400_BAD_REQUEST)

class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer