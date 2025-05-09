from rest_framework import status, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer, LoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
   
class IsManagerUser(permissions.BasePermission): 
    def has_permission(self, request, view):
        return request.user and request.user.role == 'manager'  

class IsDoctorUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'doctor'

class IsStaffUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'staff'
    
class IsNurseUser(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'nurse'

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()
    
@api_view(['POST'])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        
        user = authenticate(username=username, password=password)
        
        if user:
            refresh = RefreshToken.for_user(user)
            user_data = UserSerializer(user).data 
            
            return Response({
                'status': 'success',
                'data': {
                    'user': user_data,
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'status': 'error',
                'message': 'Thông tin đăng nhập không hợp lệ. Vui lòng thử lại'
            }, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


