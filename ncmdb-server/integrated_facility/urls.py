# urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from integrated_facility.views import EquipmentRoomsViewSet, RackViewSet, InfrastructureEquipmentViewSet, \
    ConnectionViewSet

router = DefaultRouter()
router.register(r'equipment-rooms', EquipmentRoomsViewSet, basename='equipment-rooms')
router.register(r'racks', RackViewSet, basename='racks')
router.register(r'infrastructure-equipment', InfrastructureEquipmentViewSet, basename='infrastructure-equipment')
router.register(r'connections', ConnectionViewSet, basename='connections')

urlpatterns = [
    path('', include(router.urls)),
]
