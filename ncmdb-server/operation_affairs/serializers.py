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
