from django.urls import path, include
from rest_framework.routers import DefaultRouter

from operation_affairs.views import PatrolPlanViewSet, PatrolTaskViewSet

router = DefaultRouter()
router.register(r'patrolplan/crud', PatrolPlanViewSet)
router.register(r'patroltask/crud', PatrolTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
