import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from user import permissions
from .models import NetworkDevice, Terminal, IPAM
from .serializers import NetworkDeviceSerializer, TerminalSerializer, IPAMSerializer

# 获取日志记录器
logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


class NetworkDeviceViewSet(viewsets.ModelViewSet):
    """
    网络设备 CRUD 操作 ViewSet
    """
    permission_classes = [permissions.IsNetworkEngineer]
    queryset = NetworkDevice.objects.all()
    serializer_class = NetworkDeviceSerializer
    pagination_class = CustomPagination
    search_fields = ['device_name', 'ip_address', 'model']

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
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


class IPAMViewSet(viewsets.ModelViewSet):
    """
    IP 地址管理 CRUD 操作 ViewSet
    """
    permission_classes = [permissions.IsNetworkEngineer]
    queryset = IPAM.objects.all()
    serializer_class = IPAMSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['ip_address', 'vlan', 'business_system']

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


class TerminalViewSet(viewsets.ModelViewSet):
    """
    办公终端 CRUD 操作 ViewSet
    """
    permission_classes = [permissions.IsNetworkEngineer]
    queryset = Terminal.objects.all()
    serializer_class = TerminalSerializer
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['name', 'ip_address', 'mac_address', 'vlan']

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
