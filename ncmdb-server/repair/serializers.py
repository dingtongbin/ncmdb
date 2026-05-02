from rest_framework import serializers

from .models import Notice, RepairRequest


class NoticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ['id', 'content', 'reason', 'created_at']
        read_only_fields = ['id', 'created_at']


class RepairRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = [
            'id', 'username', 'location', 'description', 'level',
            'image', 'responded', 'responded_at', 'completed',
            'completed_at', 'result', 'created_at', 'remarks'
        ]
        read_only_fields = [
            'id', 'responded', 'responded_at', 'completed',
            'completed_at', 'result', 'created_at', 'remarks'
        ]


class RepairRequestUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = RepairRequest
        fields = [
            'id', 'username', 'location', 'description', 'level',
            'image', 'responded', 'responded_at', 'completed',
            'completed_at', 'result', 'created_at', 'remarks'
        ]
        read_only_fields = ['id', 'username', 'location', 'description', 'level', 'image', 'created_at']
