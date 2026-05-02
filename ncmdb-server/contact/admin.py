from django.contrib import admin

from contact.models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'name', 'sex', 'phone1', 'phone2',
        'email', 'company', 'position', 'address'
    ]
    list_filter = ['sex', 'company']
    search_fields = ['name', 'phone1', 'phone2', 'email', 'company', 'position']
    readonly_fields = ['id']
    fieldsets = (
        ('基本信息', {
            'fields': ('name', 'sex', 'phone1', 'phone2', 'email')
        }),
        ('工作信息', {
            'fields': ('company', 'position')
        }),
        ('地址与备注', {
            'fields': ('address', 'remarks')
        }),
    )
    ordering = ['name']
