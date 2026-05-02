from rest_framework import serializers

from .models import Alert, WebhookReceiver


class AlertSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    confirm_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'
        read_only_fields = ('create_at',)


class WebhookReceiverSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = WebhookReceiver
        fields = '__all__'
        read_only_fields = ('create_at', 'update_at')
