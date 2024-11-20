from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from patient.serializers import PatientSerializer, RegisterPatientSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Patient
from accounts.views import IsManagerUser
from rest_framework.permissions import AllowAny

# Create your views here.
class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    # permission_classes = [IsManagerUser]

@api_view(['POST'])
@permission_classes([AllowAny]) 
def register_patient(request):
    serializer = RegisterPatientSerializer(data=request.data)
    
    if serializer.is_valid():
        try:
            patient = serializer.save()
            refresh = RefreshToken.for_user(patient.user)
            return Response({
                'status': 'success',
                'data': {
                    'user': {
                        'id': patient.user.id,
                        'username': patient.user.username,
                        'email': patient.user.email,
                        'role': patient.user.role,
                    },
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                    }
                }
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            return Response({
                'status': 'error',
                'message': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)