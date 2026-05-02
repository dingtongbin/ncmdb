# Register your models here.
from django.contrib import admin

from operation_affairs.models import PatrolPlan, PatrolTask


@admin.register(PatrolPlan)
class PatrolPlanAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'plan_name', 'start_time', 'end_time',
        'publisher', 'executor', 'created_at', 'updated_at'
    ]
    list_filter = ['publisher', 'executor', 'created_at']
    search_fields = ['plan_name', 'patrol_content', 'output_content']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('计划信息', {
            'fields': ('plan_name', 'start_time', 'end_time')
        }),
        ('人员信息', {
            'fields': ('publisher', 'executor')
        }),
        ('巡检内容', {
            'fields': ('patrol_content', 'output_content')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


@admin.register(PatrolTask)
class PatrolTaskAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'task_name', 'start_time', 'end_time',
        'publisher', 'executor', 'created_at', 'updated_at'
    ]
    list_filter = ['publisher', 'executor', 'created_at']
    search_fields = ['task_name', 'task_content', 'task_target']
    readonly_fields = ['id', 'created_at', 'updated_at']
    fieldsets = (
        ('任务信息', {
            'fields': ('task_name', 'start_time', 'end_time')
        }),
        ('人员信息', {
            'fields': ('publisher', 'executor')
        }),
        ('任务内容', {
            'fields': ('task_content', 'task_target')
        }),
        ('时间戳', {
            'fields': ('created_at', 'updated_at')
        }),
    )
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
