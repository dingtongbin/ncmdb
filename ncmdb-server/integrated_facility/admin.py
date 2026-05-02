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
# Register your models here.
from django.contrib import admin

from integrated_facility.models import EquipmentRooms, Rack, InfrastructureEquipment, Connection


@admin.register(EquipmentRooms)
class EquipmentRoomsAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location', 'remarks']
    list_filter = ['name']
    search_fields = ['name', 'location', 'remarks']
    readonly_fields = ['id']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'location')
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
    )
    ordering = ['id']


@admin.register(Rack)
class RackAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'equipment_room_id', 'height', 'width', 'depth', 'remarks']
    list_filter = ['equipment_room_id']
    search_fields = ['name', 'remarks']
    readonly_fields = ['id']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'equipment_room_id')
        }),
        ('尺寸规格', {
            'fields': ('height', 'width', 'depth')
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
    )
    ordering = ['id']


@admin.register(InfrastructureEquipment)
class InfrastructureEquipmentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'type', 'brand', 'model', 'serial_number',
        'device_number', 'rack_id', 'is_active'
    ]
    list_filter = ['type', 'brand', 'is_active', 'rack_id']
    search_fields = ['name', 'brand', 'model', 'serial_number', 'device_number']
    readonly_fields = ['id']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'type', 'brand', 'model', 'serial_number', 'device_number')
        }),
        ('位置信息', {
            'fields': ('rack_id', 'image')
        }),
        ('状态', {
            'fields': ('is_active',)
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
    )
    ordering = ['id']


@admin.register(Connection)
class ConnectionAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'device_id', 'home_interface', 'peer_interface',
        'peer_device', 'connection_type'
    ]
    list_filter = ['connection_type']
    search_fields = ['home_interface', 'peer_interface', 'peer_device']
    readonly_fields = ['id']
    fieldsets = (
        ('本端信息', {
            'fields': ('device_id', 'home_interface')
        }),
        ('对端信息', {
            'fields': ('peer_interface', 'peer_device')
        }),
        ('连接信息', {
            'fields': ('connection_type',)
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
    )
    ordering = ['id']
