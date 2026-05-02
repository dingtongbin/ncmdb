from django.urls import path, include
from rest_framework.routers import DefaultRouter

from alert.views import WebhookModelViewSet, AlertModelViewSet, AlertWebhookView

router = DefaultRouter()
router.register(r'webhook-crud', WebhookModelViewSet)
router.register(r'alert', AlertModelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('webhooks/', AlertWebhookView.as_view(), name='alert-webhook'),

]
