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
from django.contrib import admin

from device.models import NetworkDevice, IPAM, Terminal


@admin.register(NetworkDevice)
class NetworkDeviceAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'device_name', 'ip_address', 'mac_address', 'type', 'model',
        'sn', 'location', 'is_active', 'login_protocol', 'created_at', 'updated_at'
    ]
    list_filter = ['type', 'is_active', 'login_protocol', 'created_at']
    search_fields = ['device_name', 'ip_address', 'mac_address', 'model', 'sn', 'location']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('device_name', 'ip_address', 'mac_address', 'type', 'model', 'sn', 'location')
        }),
        ('维保信息', {
            'fields': ('maintenance_start', 'maintenance_end')
        }),
        ('本地管理', {
            'fields': ('local_admin_name', 'local_admin_password')
        }),
        ('远程登录', {
            'fields': ('login_protocol', 'login_username', 'login_password', 'login_port')
        }),
        ('系统信息', {
            'fields': ('system_info', 'is_active')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-updated_at']


@admin.register(IPAM)
class IPAMAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip_address', 'dhcp', 'reserved', 'vlan', 'business_system', 'remarks']
    list_filter = ['vlan', 'business_system']
    search_fields = ['ip_address', 'dhcp', 'business_system', 'remarks']
    readonly_fields = ['id']
    fieldsets = (
        ('IP 地址信息', {
            'fields': ('ip_address', 'dhcp', 'reserved', 'vlan', 'business_system')
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
    )
    ordering = ['id']


@admin.register(Terminal)
class TerminalAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ip_address', 'mac_address', 'vlan', 'remarks']
    list_filter = ['vlan']
    search_fields = ['name', 'ip_address', 'mac_address']
    readonly_fields = ['id']
    fieldsets = (
        ('终端信息', {
            'fields': ('name', 'ip_address', 'mac_address', 'vlan')
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
    )
    ordering = ['id']
