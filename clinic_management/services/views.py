from django.shortcuts import render
from rest_framework import viewsets
from .models import Services
from .serializers import ServicesSerializer

# Create your views here.
class ServicesViewSet(viewsets.ModelViewSet):
    queryset = Services.objects.all()
    serializer_class = ServicesSerializer