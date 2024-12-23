"""
URL configuration for clinic_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from doctor.views import DoctorViewSet
from patient.views import PatientViewSet
from appointments.views import AppointmentViewSet
from medicalrecords.views import MedicalRecordViewSet
from payments.views import PaymentViewSet
from departments.views import DepartmentViewSet
from staff.views import StaffViewSet
from accounts.views import UserViewSet, login
from manager.views import ManagerViewSet, DashboardViewSet
from services.views import ServicesViewSet
from examination.views import ExaminationViewSet
from nurse.views import NurseViewSet

router = DefaultRouter()
router.register(r'accounts', UserViewSet, basename='user')
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'doctors', DoctorViewSet, basename='doctor')
router.register(r'staffs', StaffViewSet)
router.register(r'managers', ManagerViewSet, basename='manager')
router.register(r'nurses', NurseViewSet, basename='nurse')
router.register(r'appointments', AppointmentViewSet, basename='appointment')
router.register(r'medical-records', MedicalRecordViewSet, basename='medical-record')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'services', ServicesViewSet, basename='services')
router.register(r'examination', ExaminationViewSet, basename='examination')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('auth/register/', register_patient, name='register-patient'),
    path('auth/login/',login, name='login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
