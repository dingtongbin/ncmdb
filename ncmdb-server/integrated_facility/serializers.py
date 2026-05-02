from rest_framework import serializers

from integrated_facility.models import EquipmentRooms, Rack, InfrastructureEquipment, Connection


class EquipmentRoomsSerializer(serializers.ModelSerializer):
    """
    机房序列化器
    """
    rack_count = serializers.SerializerMethodField()

    def get_rack_count(self, obj):
        # 手动统计该设备间下的机柜数量
        return Rack.objects.filter(equipment_room_id=obj.id).count()

    class Meta:
        model = EquipmentRooms
        fields = '__all__'


class RackSerializer(serializers.ModelSerializer):
    """
    机柜序列化器
    """
    device_count = serializers.SerializerMethodField()

    def get_device_count(self, obj):
        # 统计该机柜下的设备数量
        return InfrastructureEquipment.objects.filter(rack_id=obj.id).count()

    class Meta:
        model = Rack
        fields = '__all__'


class InfrastructureEquipmentSerializer(serializers.ModelSerializer):
    """
    基础设施设备序列化器
    """

    class Meta:
        model = InfrastructureEquipment
        fields = '__all__'


class ConnectionSerializer(serializers.ModelSerializer):
    """
    基础设施连接信息序列化器
    """

    class Meta:
        model = Connection
        fields = '__all__'
