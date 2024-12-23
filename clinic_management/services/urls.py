from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ServicesViewSet

router = DefaultRouter()
router.register(r'', ServicesViewSet, basename='services')

urlpatterns = [
    path('', include(router.urls)),
]