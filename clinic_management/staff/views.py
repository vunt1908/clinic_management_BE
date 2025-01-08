from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import StaffSerializer
from .models import Staff

class StaffViewSet(viewsets.ModelViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Thêm mới nhân viên thành công.',
            'data': StaffSerializer(staff).data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        staff = serializer.save()
        
        return Response({
            'status': 'success',
            'message': 'Cập nhật thông tin nhân viên thành công.',
            'data': StaffSerializer(staff).data
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
                'message': 'Xoá thành công nhân viên.'
            }, status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = Staff.objects.all()
        return queryset