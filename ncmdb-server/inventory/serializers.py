from rest_framework import serializers

from inventory.models import InventoryItem, InventoryRecord


class InventoryItemSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = InventoryItem
        fields = '__all__'


class InventoryRecordSerializer(serializers.ModelSerializer):
    operation_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    operator_name = serializers.CharField(source='operator.real_name', read_only=True)
    operator_username = serializers.CharField(source='operator.username', read_only=True)
    item_name = serializers.CharField(source='inventory_item.name', read_only=True)
    item_type = serializers.CharField(source='inventory_item.item_type', read_only=True)

    class Meta:
        model = InventoryRecord
        fields = '__all__'
