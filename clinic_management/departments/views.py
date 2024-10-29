from django.shortcuts import render
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from .models import Department
from .serializers import DepartmentSerializer
from accounts.serializers import DoctorSerializer

# Create your views here.
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

  