from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import NetworkDeviceViewSet, IPAMViewSet, TerminalViewSet

router = DefaultRouter()
router.register(r'network', NetworkDeviceViewSet)
router.register(r'ipam', IPAMViewSet)
router.register(r'terminal', TerminalViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
