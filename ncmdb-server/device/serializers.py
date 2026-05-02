from rest_framework import serializers

from .models import NetworkDevice, IPAM, Terminal


class NetworkDeviceSerializer(serializers.ModelSerializer):
    """
    网络设备序列化器
    """
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    maintenance_start = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)
    maintenance_end = serializers.DateField(format="%Y-%m-%d", required=False, allow_null=True)

    class Meta:
        model = NetworkDevice
        fields = '__all__'


class IPAMSerializer(serializers.ModelSerializer):
    """
    IP 地址管理序列化器
    """

    class Meta:
        model = IPAM
        fields = '__all__'


class TerminalSerializer(serializers.ModelSerializer):
    """
    办公终端序列化器
    """

    class Meta:
        model = Terminal
        fields = '__all__'
