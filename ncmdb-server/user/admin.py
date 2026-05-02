from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.models import User


# Register your models here.
class CustomUserAdmin(UserAdmin):
    # 配置管理界面显示字段
    list_display = ('username', 'real_name', 'is_staff', 'is_superuser', 'is_network_engineer', 'is_active')

    # 添加筛选器
    list_filter = ('is_staff', 'is_superuser', 'is_network_engineer', 'is_active', 'department')

    # 重新定义字段集，只包含自定义用户模型中存在的字段
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('real_name', 'phone', 'department')}),
        ('权限',
         {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_network_engineer', 'groups', 'user_permissions')}),
    )

    # 创建用户时的字段配置
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'real_name', 'phone', 'department', 'password1', 'password2', 'is_staff',
                       'is_network_engineer'),
        }),
    )

    # 指定搜索字段
    search_fields = ('username', 'real_name')

    # 指定排序字段
    ordering = ('username',)

    def get_model_perms(self, request):
        # 确保模型权限正确设置
        return super().get_model_perms(request)


admin.site.register(User, CustomUserAdmin)

admin.site.site_title = '网络运维资产管理系统'  # 页面标题（浏览器标签页）
admin.site.site_header = '网络运维资产管理系统'  # 页面顶部标题
admin.site.index_title = '网络运维资产管理系统'  # 首页标题
