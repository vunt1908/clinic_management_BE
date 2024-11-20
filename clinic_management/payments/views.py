from rest_framework import viewsets
from .serializers import PaymentSerializer
from accounts.views import IsManagerUser, IsStaffUser
from .models import Payment

# Create your views here.
class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer

    # def get_permissions(self):
    #     if self.action in ['update', 'partial_update']:
    #         permission_classes = [IsStaffUser]
    #     else:
    #         permission_classes = [IsManagerUser] 
    #     return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        # user = self.request.user
        # if user.role == 'manager':
        #     return Payment.objects.all()
        # elif user.role == 'staff':
        #     return Payment.objects.all()
        # elif user.role == 'patient':
        #     return Payment.objects.filter(appointment__patient__user=user)
        # return Payment.objects.none()
        return Payment.objects.all()