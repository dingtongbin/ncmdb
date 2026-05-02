from django.db.models import Q
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination

from user import permissions
from user.permissions import IsNetworkEngineer
from .models import WorkOrder, WorkOrderEvaluation, WorkOrderHandleLog


@api_view(['POST'])
@permission_classes([permissions.IsNormalUser])
def create_work_order(request):
    try:
        # 从 JWT token 中获取当前登录用户
        user = request.user
        # 获取请求数据
        location = request.data.get('location')
        level = request.data.get('level')
        description = request.data.get('description')
        # 验证必填字段
        if not location or not location.strip():
            return JsonResponse({
                'success': False,
                'error': '故障地点不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not description or not description.strip():
            return JsonResponse({
                'success': False,
                'error': '故障描述不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        if not level:
            return JsonResponse({
                'success': False,
                'error': '紧急程度不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 验证紧急程度的有效性
        valid_levels = ['low', 'normal', 'high', 'urgent']
        if level not in valid_levels:
            return JsonResponse({
                'success': False,
                'error': f'紧急程度必须是：{", ".join(valid_levels)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        # 创建工单
        work_order = WorkOrder.objects.create(
            user=user,  # 直接关联用户对象
            location=location.strip(),
            level=level,
            description=description.strip(),
            status='pending',
        )
        # 返回成功响应
        return JsonResponse({
            'success': True,
            'message': '工单提交成功',
            'data': {
                'work_order_no': work_order.work_order_no,
                'status': work_order.get_status_display(),
                'level': work_order.get_level_display(),
                'location': work_order.location,
                'created_at': work_order.created_at.strftime('%Y-%m-%d %H:%M:%S')
            }
        }, status=status.HTTP_201_CREATED)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'工单提交失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsNormalUser])
def get_my_work_orders(request):
    try:
        # 查询当前用户的所有工单，按创建时间倒序
        work_orders = WorkOrder.objects.filter(
            user=request.user
        ).order_by('-created_at')

        # 序列化数据
        data = []
        for order in work_orders:
            data.append({
                'id': order.id,
                'work_order_no': order.work_order_no,
                'location': order.location,
                'description': order.description,
                'level': order.level,
                'level_display': order.get_level_display(),
                'status': order.status,
                'status_display': order.get_status_display(),
                'result': order.result or '',
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'completed_at': order.completed_at.strftime('%Y-%m-%d %H:%M:%S') if order.completed_at else None
            })

        return JsonResponse(data, safe=False)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'查询失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([permissions.IsNormalUser])
def get_work_order_detail(request, id):
    try:
        # 查询工单
        work_order = WorkOrder.objects.get(id=id)

        # 验证权限：只能查看自己的工单
        if work_order.user != request.user:
            return JsonResponse({
                'success': False,
                'error': '无权查看此工单'
            }, status=status.HTTP_403_FORBIDDEN)

        # 检查是否有评价
        has_evaluated = WorkOrderEvaluation.objects.filter(work_order=work_order).exists()

        # 获取处理记录
        handle_logs = []
        for log in work_order.handle_logs.all():
            handle_logs.append({
                'id': log.id,
                'handler_name': log.handler.real_name if log.handler else log.handler_name,
                'handle_type': log.handle_type,
                'handle_type_display': log.get_handle_type_display(),
                'content': log.content,
                'handle_at': log.handle_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        # 构造返回数据
        data = {
            'id': work_order.id,
            'work_order_no': work_order.work_order_no,
            'username': work_order.user.username if work_order.user else '',
            'name': work_order.user.real_name if work_order.user else '',
            'phone': work_order.user.phone if work_order.user else '',
            'location': work_order.location,
            'description': work_order.description,
            'level': work_order.level,
            'level_display': work_order.get_level_display(),
            'status': work_order.status,
            'status_display': work_order.get_status_display(),
            'result': work_order.result or '',
            'created_at': work_order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': work_order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
            'completed_at': work_order.completed_at.strftime('%Y-%m-%d %H:%M:%S') if work_order.completed_at else None,
            'has_evaluated': has_evaluated,
            'handle_logs': handle_logs
        }

        return JsonResponse(data, safe=False)

    except WorkOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '工单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'查询失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([permissions.IsNormalUser])
def submit_evaluation(request, id):
    """
    提交工单评价

    接口说明：
    - 请求方式：POST
    - 权限要求：必须登录（通过 JWT 认证）
    - 功能：用户对已完成的工单进行评价

    路径参数：
    - id: 工单 ID

    请求参数：
    - satisfaction: 满意度 (必填，整数 1-5)
    - content: 评价内容 (可选，字符串)

    """
    try:
        # 查询工单
        work_order = WorkOrder.objects.get(id=id)

        # 验证权限：只能评价自己的工单
        if work_order.user != request.user:
            return JsonResponse({
                'success': False,
                'error': '无权操作此工单'
            }, status=status.HTTP_403_FORBIDDEN)
        # 验证工单状态：只有已完成的工单才能评价
        if work_order.status != 'completed':
            return JsonResponse({
                'success': False,
                'error': '只有已完成的工单才能评价'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 检查是否已经评价过
        if WorkOrderEvaluation.objects.filter(work_order=work_order).exists():
            return JsonResponse({
                'success': False,
                'error': '您已经评价过此工单'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 获取请求数据
        satisfaction = request.data.get('satisfaction')
        content = request.data.get('content', '')

        # 验证必填字段
        if not satisfaction:
            return JsonResponse({
                'success': False,
                'error': '满意度评分不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 验证评分范围
        try:
            satisfaction = int(satisfaction)
            if not (1 <= satisfaction <= 5):
                raise ValueError()
        except (ValueError, TypeError):
            return JsonResponse({
                'success': False,
                'error': '满意度评分必须是 1-5 的整数'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 创建评价
        evaluation = WorkOrderEvaluation.objects.create(
            work_order=work_order,
            satisfaction=satisfaction,
            content=content.strip() if content else ''
        )

        # 返回成功响应
        return JsonResponse({
            'success': True,
            'message': '评价提交成功',
            'data': {
                'evaluation_id': evaluation.id,
                'satisfaction': evaluation.satisfaction,
                'content': evaluation.content
            }
        }, status=status.HTTP_201_CREATED)

    except WorkOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '工单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'评价提交失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class WorkOrderPagination(PageNumberPagination):
    """工单分页器"""
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100



@api_view(['GET'])
@permission_classes([IsNetworkEngineer])
def get_engineer_work_orders(request):
    try:
        # 获取查询参数
        status_filter = request.query_params.get('status', None)
        level_filter = request.query_params.get('level', None)
        keyword = request.query_params.get('keyword', None)
        assignee_id = request.query_params.get('assignee_id', None)

        # 基础查询集
        work_orders = WorkOrder.objects.all()

        # 状态筛选
        if status_filter:
            work_orders = work_orders.filter(status=status_filter)

        # 紧急程度筛选
        if level_filter:
            work_orders = work_orders.filter(level=level_filter)

        # 关键词搜索
        if keyword:
            work_orders = work_orders.filter(
                Q(work_order_no__icontains=keyword) |
                Q(user__real_name__icontains=keyword) |
                Q(user__username__icontains=keyword) |
                Q(location__icontains=keyword)
            )

        # 处理人筛选
        if assignee_id:
            work_orders = work_orders.filter(assignee_id=assignee_id)

        # 分页
        paginator = WorkOrderPagination()
        page = paginator.paginate_queryset(work_orders.order_by('-created_at'), request)

        # 序列化数据
        data = []
        for order in page:
            data.append({
                'id': order.id,
                'work_order_no': order.work_order_no,
                'username': order.user.username if order.user else '',
                'name': order.user.real_name if order.user else '',
                'phone': order.user.phone if order.user else '',
                'department': order.user.department if order.user else '',
                'location': order.location,
                'description': order.description,
                'level': order.level,
                'level_display': order.get_level_display(),
                'status': order.status,
                'status_display': order.get_status_display(),
                'assignee': order.assignee_id,
                'assignee_name': order.assignee.real_name if order.assignee else None,
                'result': order.result or '',
                'created_at': order.created_at.strftime('%Y-%m-%d %H:%M:%S'),
                'updated_at': order.updated_at.strftime('%Y-%m-%d %H:%M:%S'),
                'completed_at': order.completed_at.strftime('%Y-%m-%d %H:%M:%S') if order.completed_at else None
            })

        return paginator.get_paginated_response(data)

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'查询失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def accept_work_order(request, id):
    """
    网络工程师接单（待受理 -> 已受理）

    接口说明：
    - 请求方式：POST
    - 权限要求：网络工程师或管理员
    - 功能：网络工程师接单，将工单状态改为已受理

    路径参数：
    - id: 工单 ID

    返回示例：
    {
        "success": true,
        "message": "接单成功",
        "data": {
            "work_order_no": "000001",
            "status": "accepted",
            "status_display": "已受理",
            "assignee_name": "李工"
        }
    }
    """
    try:
        # 查询工单
        work_order = WorkOrder.objects.get(id=id)

        # 验证状态：只有待受理的工单才能接单
        if work_order.status != 'pending':
            return JsonResponse({
                'success': False,
                'error': '只有待受理的工单才能接单'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新工单状态
        work_order.status = 'accepted'
        work_order.assignee = request.user
        work_order.save()

        # 创建处理记录
        WorkOrderHandleLog.objects.create(
            work_order=work_order,
            handler=request.user,
            # handler_name=request.user.real_name,
            handle_type='diagnose',
            content='接单受理'
        )

        return JsonResponse({
            'success': True,
            'message': '接单成功',
            'data': {
                'work_order_no': work_order.work_order_no,
                'status': work_order.status,
                'status_display': work_order.get_status_display(),
                'assignee_name': work_order.assignee.real_name
            }
        }, status=status.HTTP_200_OK)

    except WorkOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '工单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'接单失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsNetworkEngineer])
def submit_work_order_result(request, id):
    """
    网络工程师提交处理结果（处理中 -> 已完成）

    接口说明：
    - 请求方式：POST
    - 权限要求：网络工程师或管理员
    - 功能：提交处理结果，将工单状态改为已完成

    路径参数：
    - id: 工单 ID

    请求参数：
    - result: 处理结果 (必填)
    - handle_type: 处理类型 (可选，diagnose/repair/configure/other)
    - content: 处理内容 (可选)

    返回示例：
    {
        "success": true,
        "message": "处理结果提交成功",
        "data": {
            "work_order_no": "000001",
            "status": "completed",
            "status_display": "已完成",
            "result": "已修复网络故障"
        }
    }
    """
    try:
        # 查询工单
        work_order = WorkOrder.objects.get(id=id)

        # 验证权限：只能处理分配给自己的工单
        if work_order.assignee != request.user and not (request.user.is_staff or request.user.is_superuser):
            return JsonResponse({
                'success': False,
                'error': '无权操作此工单'
            }, status=status.HTTP_403_FORBIDDEN)

        # 获取请求数据
        result = request.data.get('result', '')
        handle_type = request.data.get('handle_type', 'other')
        content = request.data.get('content', '')

        # 验证必填字段
        if not result or not result.strip():
            return JsonResponse({
                'success': False,
                'error': '处理结果不能为空'
            }, status=status.HTTP_400_BAD_REQUEST)

        # 更新工单
        work_order.status = 'completed'
        work_order.result = result.strip()
        work_order.completed_at = timezone.now()
        work_order.save()

        # 创建处理记录
        WorkOrderHandleLog.objects.create(
            work_order=work_order,
            handler=request.user,
            handle_type=handle_type,
            content=content.strip() if content else f'提交处理结果：{result}'
        )

        return JsonResponse({
            'success': True,
            'message': '处理结果提交成功',
            'data': {
                'work_order_no': work_order.work_order_no,
                'status': work_order.status,
                'status_display': work_order.get_status_display(),
                'result': work_order.result
            }
        }, status=status.HTTP_200_OK)

    except WorkOrder.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': '工单不存在'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': f'提交失败：{str(e)}'
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
