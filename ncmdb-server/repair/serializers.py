# Copyright 2026 dingtongbin
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
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
