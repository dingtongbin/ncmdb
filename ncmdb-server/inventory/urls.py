from django.urls import path, include
from rest_framework.routers import DefaultRouter

from inventory.views import InventoryItemModelViewSet, InventoryRecordViewSet

router = DefaultRouter()
router.register(r'item', InventoryItemModelViewSet, basename='inventory-item')
router.register(r'record', InventoryRecordViewSet, basename='inventory-record')

urlpatterns = [
    path('', include(router.urls)),
]
