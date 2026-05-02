import hashlib
import secrets

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from alert.models import WebhookReceiver, Alert
from alert.serializers import WebhookReceiverSerializer, AlertSerializer
from user import permissions


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class WebhookModelViewSet(viewsets.ModelViewSet):
    queryset = WebhookReceiver.objects.all()
    serializer_class = WebhookReceiverSerializer
    permission_classes = [permissions.IsNetworkEngineer]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['name', 'create_at', 'source']

    def create(self, request, *args, **kwargs):
        """
        重写create方法，自动生成128位长度的哈希token
        """
        # 复制请求数据
        data = request.data.copy()
        # 生成随机字符串并进行SHA256哈希，取前128位
        random_string = secrets.token_hex(64)  # 生成128字节的随机字符串
        hash_token = hashlib.sha256(random_string.encode()).hexdigest()[:32]  # 取前32个字符（128位）
        data['secret_token'] = hash_token

        # 使用修改后的数据创建serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """
        通用批量删除方法，支持任意主键字段
        """
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'error': '请选择要删除的记录'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 获取模型类和主键字段名
        model_class = self.queryset.model
        primary_key_field = model_class._meta.pk.name

        # 构造查询条件
        filter_kwargs = {f'{primary_key_field}__in': ids}
        deleted_count, _ = model_class.objects.filter(**filter_kwargs).delete()

        return Response(
            {'message': f'成功删除 {deleted_count} 条记录'},
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        """
        重写 create 方法，自动生成 128 位长度的哈希 token
        """
        # 复制请求数据
        data = request.data.copy()

        # 如果没有提供 api_token 或为空，则生成 128 位哈希 token
        if not data.get('api_token'):
            # 生成随机字符串并进行 SHA256 哈希，取前 128 位
            random_string = secrets.token_hex(64)  # 生成 128 字节的随机字符串
            hash_token = hashlib.sha256(random_string.encode()).hexdigest()[:32]  # 取前 32 个字符（128 位）
            data['api_token'] = hash_token

        # 使用修改后的数据创建 serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class AlertModelViewSet(viewsets.ModelViewSet):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [permissions.IsNetworkEngineer]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['source', 'severity', 'source', 'title', 'description', 'host', 'ip']

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """
        通用批量删除方法，支持任意主键字段
        """
        ids = request.data.get('ids', [])
        if not ids:
            return Response(
                {'error': '请选择要删除的记录'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 获取模型类和主键字段名
        model_class = self.queryset.model
        primary_key_field = model_class._meta.pk.name

        # 构造查询条件
        filter_kwargs = {f'{primary_key_field}__in': ids}
        deleted_count, _ = model_class.objects.filter(**filter_kwargs).delete()

        return Response(
            {'message': f'成功删除 {deleted_count} 条记录'},
            status=status.HTTP_200_OK
        )


# views.py
from django.http import JsonResponse
import json
import logging
from .models import WebhookReceiver, Alert

logger = logging.getLogger(__name__)


class AlertWebhookView(APIView):
    permission_classes = []

    def post(self, request):
        try:
            # 解析请求数据
            try:
                if request.content_type == 'application/json':
                    data = json.loads(request.body)
                else:
                    data = request.POST.dict()
            except Exception as e:
                logger.error(f"Failed to parse request data: {e}")
                return JsonResponse({
                    'success': False,
                    'message': '请求数据格式错误'
                }, status=400)

            # 1. 检查 api_token 是否存在
            api_token = data.get('api_token')
            if not api_token:
                return JsonResponse({
                    'success': False,
                    'message': '缺少api_token参数'
                }, status=400)

            # 2. 验证 api_token 是否存在且有效
            try:
                receiver = WebhookReceiver.objects.get(api_token=api_token)
            except WebhookReceiver.DoesNotExist:
                logger.warning(f"Webhook token not found: {api_token}")
                return JsonResponse({
                    'success': False,
                    'message': '无效的API令牌'
                }, status=401)

            # 3. 检查是否禁用
            if not receiver.is_active:
                logger.warning(f"Webhook receiver is disabled: {receiver.name}")
                return JsonResponse({
                    'success': False,
                    'message': '该webhook接收器已被禁用'
                }, status=403)

            # 4. 校验必要参数
            if 'title' not in data:
                return JsonResponse({
                    'success': False,
                    'message': '缺少必要参数: title'
                }, status=400)

            if 'raw_data' not in data:
                return JsonResponse({
                    'success': False,
                    'message': '缺少必要参数: raw_data'
                }, status=400)

            # 5. 创建告警记录
            alert_data = {
                'title': data['title'],
                'raw_data': data.get('raw_data', {}),
                'source': receiver.source,
            }

            # 处理可选参数，使用模型默认值或空值
            optional_fields = ['severity', 'status', 'description', 'host', 'ip']
            for field in optional_fields:
                if field in data:
                    alert_data[field] = data[field]
                # 如果不在数据中，模型会自动使用默认值或空值

            # 创建告警
            alert = Alert.objects.create(**alert_data)

            logger.info(f"Successfully created alert: {alert.title}")
            return JsonResponse({
                'success': True,
                'message': '告警创建成功',
                'alert_id': alert.id
            }, status=201)

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return JsonResponse({
                'success': False,
                'message': '服务器内部错误'
            }, status=500)
