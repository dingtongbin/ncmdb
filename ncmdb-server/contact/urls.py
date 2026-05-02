from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import ContactModelViewSet

router = DefaultRouter()
router.register(r'crud', ContactModelViewSet)

urlpatterns = [
    path('', include(router.urls)),

]
