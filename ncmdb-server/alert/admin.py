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

from alert.models import Alert, WebhookReceiver


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'source', 'severity', 'status',
        'host', 'ip', 'created_at', 'confirm_at'
    ]
    list_filter = ['source', 'severity', 'status', 'created_at']
    search_fields = ['title', 'description', 'host', 'ip', 'raw_data']
    readonly_fields = ['id', 'created_at', 'confirm_at', 'raw_data']
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'source', 'severity', 'status')
        }),
        ('告警详情', {
            'fields': ('description', 'host', 'ip')
        }),
        ('原始数据', {
            'fields': ('raw_data',),
            'classes': ('collapse',)
        }),
        ('时间戳', {
            'fields': ('created_at', 'confirm_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(WebhookReceiver)
class WebhookReceiverAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'source', 'is_active', 'created_at', 'updated_at']
    list_filter = ['source', 'is_active', 'created_at']
    search_fields = ['name', 'source', 'remarks']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'source', 'is_active')
        }),
        ('认证信息', {
            'fields': ('api_token',)
        }),
        ('备注', {
            'fields': ('remarks',)
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'updated_at'
    ordering = ['-updated_at']
