# Register your models here.
from django.contrib import admin

from repair.models import WorkOrder, WorkOrderHandleLog, WorkOrderEvaluation


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'work_order_no', 'user', 'location', 'level',
        'status', 'assignee', 'created_at', 'updated_at', 'completed_at'
    ]
    list_filter = ['status', 'level', 'created_at', 'completed_at']
    search_fields = ['work_order_no', 'location', 'description', 'user__username', 'user__real_name']
    readonly_fields = ['id', 'work_order_no', 'created_at', 'updated_at', 'completed_at']
    fieldsets = (
        ('工单信息', {
            'fields': ('work_order_no', 'user', 'location')
        }),
        ('故障信息', {
            'fields': ('description', 'level')
        }),
        ('分配信息', {
            'fields': ('assignee', 'status')
        }),
        ('处理结果', {
            'fields': ('result',)
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at', 'completed_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(WorkOrderHandleLog)
class WorkOrderHandleLogAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'work_order', 'handler', 'handle_type', 'handle_at'
    ]
    list_filter = ['handle_type', 'handle_at']
    search_fields = ['content', 'handler__username', 'handler__real_name', 'work_order__work_order_no']
    readonly_fields = ['id', 'handle_at']
    fieldsets = (
        ('工单信息', {
            'fields': ('work_order',)
        }),
        ('处理信息', {
            'fields': ('handler', 'handle_type', 'content')
        }),
        ('时间', {
            'fields': ('handle_at',)
        }),
    )
    date_hierarchy = 'handle_at'
    ordering = ['-handle_at']


@admin.register(WorkOrderEvaluation)
class WorkOrderEvaluationAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_order', 'satisfaction', 'content', 'created_at']
    list_filter = ['satisfaction', 'created_at']
    search_fields = ['content', 'work_order__work_order_no']
    readonly_fields = ['id', 'created_at']
    fieldsets = (
        ('工单信息', {
            'fields': ('work_order',)
        }),
        ('评价信息', {
            'fields': ('satisfaction', 'content')
        }),
        ('时间', {
            'fields': ('created_at',)
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
