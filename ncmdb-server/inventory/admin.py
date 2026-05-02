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

from inventory.models import InventoryItem, InventoryRecord


@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'item_type', 'location', 'quantity',
        'unit', 'created_at', 'updated_at'
    ]
    list_filter = ['item_type', 'location', 'created_at']
    search_fields = ['name', 'item_type', 'location', 'remarks']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'item_type', 'location', 'quantity', 'unit')
        }),
        ('图片', {
            'fields': ('image',)
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(InventoryRecord)
class InventoryRecordAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'inventory_item', 'record_type', 'quantity',
        'operator', 'operation_time', 'remarks'
    ]
    list_filter = ['record_type', 'operation_time']
    search_fields = [
        'inventory_item__name', 'operator__username',
        'operator__real_name', 'remarks'
    ]
    readonly_fields = ['id', 'operation_time']
    fieldsets = (
        ('记录信息', {
            'fields': ('inventory_item', 'record_type', 'quantity')
        }),
        ('操作人', {
            'fields': ('operator',)
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
        ('时间', {
            'fields': ('operation_time',)
        }),
    )
    date_hierarchy = 'operation_time'
    ordering = ['-operation_time']
