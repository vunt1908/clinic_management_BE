from django.urls import path, include
from .views import UserViewSet, PatientViewSet, DoctorViewSet, StaffViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'patients', PatientViewSet, basename='patients')
router.register(r'doctors',DoctorViewSet, basename='doctors')
router.register(r'staffs', StaffViewSet, basename='staff')

urlpatterns = [
    path('', include(router.urls)),
]