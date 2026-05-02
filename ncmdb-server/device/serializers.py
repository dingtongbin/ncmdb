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
