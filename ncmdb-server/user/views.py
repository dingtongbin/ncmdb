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
# views.py
import os
import re
from datetime import datetime, timedelta

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from alert.models import Alert
from device.models import NetworkDevice
from integrated_facility.models import EquipmentRooms, Rack, InfrastructureEquipment
from repair.models import WorkOrder
from user.permissions import IsNetworkEngineer


@method_decorator(csrf_exempt, name='dispatch')
class NetworkEngineerUpload(View):
    """
    网络工程师文件上传接口
    """

    def post(self, request):
        try:
            # 获取上传的文件
            uploaded_file = request.FILES.get('file')

            if not uploaded_file:
                return JsonResponse({
                    'status': 'error',
                    'message': '未找到上传文件'
                }, status=400)

            # 确保 media 目录存在
            media_root = settings.MEDIA_ROOT
            network_engineer_dir = os.path.join(media_root, 'network_engineer')

            if not os.path.exists(network_engineer_dir):
                os.makedirs(network_engineer_dir)

            # 保存文件到指定目录
            file_path = os.path.join(network_engineer_dir, uploaded_file.name)
            path = default_storage.save(file_path, ContentFile(uploaded_file.read()))

            # 返回成功响应
            return JsonResponse({
                'status': 'success',
                'message': '文件上传成功',
                'file_path': 'http://127.0.0.1:8000' + os.path.join(settings.MEDIA_URL, 'network_engineer',
                                                                    uploaded_file.name),
                'file_name': uploaded_file.name
            })

        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': f'文件上传失败: {str(e)}'
            }, status=500)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def check_user_role(request):
    """
    判断登录人员的角色：管理员、网络工程师、普通用户
    """
    user = request.user

    # 检查是否是管理员或超级用户
    is_admin_or_super = user.is_staff or user.is_superuser

    # 检查是否是网络工程师组成员
    is_network_engineer = user.groups.filter(name='Network Engineer').exists()

    # 判断角色
    if is_admin_or_super:
        role = 'admin'
        role_description = '管理员'
    elif is_network_engineer:
        role = 'network_engineer'
        role_description = '网络工程师'
    else:
        role = 'normal_user'
        role_description = '普通用户'

    print("=" * 60)
    print("🔵 DEBUG: 检查用户角色")
    print(f"👤 用户：{user.username} ({user.real_name})")
    print(f"🎭 角色：{role} - {role_description}")
    print(f"✔️ 是管理员/超级用户：{is_admin_or_super}")
    print(f"✔️ 是网络工程师组成员：{is_network_engineer}")
    print("=" * 60)

    return JsonResponse({
        'status': 'success',
        'data': {
            'user_id': user.id,
            'username': user.username,
            'real_name': user.real_name,
            'role': role,
            'role_description': role_description,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
            'is_network_engineer': is_network_engineer,
            'groups': list(user.groups.all().values_list('name', flat=True))
        }
    })


# ... existing code ...
@api_view(['GET'])
@permission_classes([IsNetworkEngineer])
def get_statistics_data(request):
    """
    获取统计数据：网络设备、设备间、机柜、机房设施数量，以及最近六个月的故障和报修数量
    只允许网络工程师访问
    确保输出最近六个月的数据，如果某个月没有数据则补 0

    返回示例：
    {
        "network_device_count": 120,
        "equipment_room_count": 15,
        "rack_count": 30,
        "infrastructure_count": 20,
        "alert_stats": [
            {"month": "2025-01", "count": 5},
            {"month": "2025-02", "count": 8},
            {"month": "2025-03", "count": 0},
            {"month": "2025-04", "count": 12},
            {"month": "2025-05", "count": 9},
            {"month": "2025-06", "count": 15}
        ],
        "work_order_stats": [
            {"month": "2025-01", "count": 3},
            {"month": "2025-02", "count": 0},
            {"month": "2025-03", "count": 7},
            {"month": "2025-04", "count": 5},
            {"month": "2025-05", "count": 11},
            {"month": "2025-06", "count": 8}
        ]
    }
    """
    try:
        # 获取网络设备数量
        network_device_count = NetworkDevice.objects.filter(is_active=True).count()

        # 获取设备间数量
        equipment_room_count = EquipmentRooms.objects.count()

        # 获取机柜数量
        rack_count = Rack.objects.count()

        # 获取机房设施数量
        infrastructure_count = InfrastructureEquipment.objects.filter(is_active=True).count()

        # 生成最近六个月的月份列表（包含当前月）
        current_date = datetime.now()
        month_list = []
        for i in range(5, -1, -1):
            # 计算每个月的第一天
            if current_date.month - i <= 0:
                # 需要跨年到前一年
                month_date = current_date.replace(
                    year=current_date.year - 1,
                    month=current_date.month + 12 - i,
                    day=1
                )
            else:
                month_date = current_date.replace(
                    month=current_date.month - i,
                    day=1
                )
            month_str = month_date.strftime('%Y-%m')
            month_list.append(month_str)

        # 获取最近六个月的告警统计
        six_months_ago = current_date - timedelta(days=180)
        alert_stats_raw = Alert.objects.filter(
            created_at__gte=six_months_ago
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        # 获取最近六个月的工单统计
        work_order_stats_raw = WorkOrder.objects.filter(
            created_at__gte=six_months_ago
        ).annotate(
            month=TruncMonth('created_at')
        ).values('month').annotate(
            count=Count('id')
        ).order_by('month')

        # 格式化数据，确保六个月数据完整
        def format_stats_with_complete_months(stats_raw, months):
            # 创建月份到数量的映射
            month_to_count = {}
            for item in stats_raw:
                month_str = item['month'].strftime('%Y-%m')
                month_to_count[month_str] = item['count']

            # 确保所有月份都有数据，没有的补 0
            result = []
            for month in months:
                result.append({
                    'month': month,
                    'count': month_to_count.get(month, 0)
                })

            return result

        return Response({
            'network_device_count': network_device_count,
            'equipment_room_count': equipment_room_count,
            'rack_count': rack_count,
            'infrastructure_count': infrastructure_count,
            'alert_stats': format_stats_with_complete_months(alert_stats_raw, month_list),
            'work_order_stats': format_stats_with_complete_months(work_order_stats_raw, month_list)
        })

    except Exception as e:
        return Response(
            {'error': f'获取统计数据失败：{str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ... existing code ...

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_info(request):
    """
    获取当前登录用户的工号和真实姓名
    """
    try:
        user = request.user

        return JsonResponse({
            'status': 'success',
            'data': {
                'user_id': user.id,
                'username': user.username,
                'real_name': user.real_name,
                'department': user.department,
                'phone': user.phone
            }
        })

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'获取用户信息失败：{str(e)}'
        }, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    用户修改密码接口
    只允许网络管理员和普通用户访问
    需要输入旧密码和两次新密码
    密码必须是 8 位且包含大小写字母和数字
    """
    try:
        user = request.user

        # 检查是否是管理员或普通用户（排除某些特殊用户）
        # 由于使用了 JWT 认证，只要是已认证用户都可以访问
        if not user.is_authenticated:
            return JsonResponse({
                'status': 'error',
                'message': '请先登录'
            }, status=401)

        # 获取请求数据
        data = request.data
        old_password = data.get('old_password')
        new_password1 = data.get('new_password1')
        new_password2 = data.get('new_password2')

        # 验证必填字段
        if not old_password or not new_password1 or not new_password2:
            return JsonResponse({
                'status': 'error',
                'message': '旧密码、新密码和确认新密码都是必填项'
            }, status=400)

        # 验证两次新密码是否一致
        if new_password1 != new_password2:
            return JsonResponse({
                'status': 'error',
                'message': '两次输入的新密码不一致'
            }, status=400)

        # 验证新密码长度
        if len(new_password1) < 8:
            return JsonResponse({
                'status': 'error',
                'message': '密码长度至少为 8 位'
            }, status=400)

        # 验证新密码复杂度：必须包含大小写字母和数字
        if not re.search(r'[a-z]', new_password1):
            return JsonResponse({
                'status': 'error',
                'message': '密码必须包含小写字母'
            }, status=400)

        if not re.search(r'[A-Z]', new_password1):
            return JsonResponse({
                'status': 'error',
                'message': '密码必须包含大写字母'
            }, status=400)

        if not re.search(r'[0-9]', new_password1):
            return JsonResponse({
                'status': 'error',
                'message': '密码必须包含数字'
            }, status=400)

        # 验证旧密码是否正确
        if not user.check_password(old_password):
            return JsonResponse({
                'status': 'error',
                'message': '旧密码错误'
            }, status=400)

        # 设置新密码
        user.set_password(new_password1)
        user.save()

        return JsonResponse({
            'status': 'success',
            'message': '密码修改成功，请重新登录'
        }, status=200)

    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'修改密码失败：{str(e)}'
        }, status=500)
