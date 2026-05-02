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
