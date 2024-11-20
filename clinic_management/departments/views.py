from rest_framework import viewsets
from .models import Department
from .serializers import DepartmentSerializer

# Create your views here.
class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

  