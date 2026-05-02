from rest_framework import serializers

from .models import PatrolPlan, PatrolTask


class PatrolPlanSerializer(serializers.ModelSerializer):
    """
    巡检计划序列化器
    """
    start_time = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    end_time = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = PatrolPlan
        fields = '__all__'


class PatrolTaskSerializer(serializers.ModelSerializer):
    """
    计划任务序列化器
    """
    start_time = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    end_time = serializers.DateTimeField(format="%Y-%m-%d", required=False)
    updated_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = PatrolTask
        fields = '__all__'
