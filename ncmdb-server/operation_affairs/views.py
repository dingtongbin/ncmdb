import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from user import permissions
from .models import PatrolPlan, PatrolTask
from .serializers import PatrolPlanSerializer, PatrolTaskSerializer

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 500


class PatrolPlanViewSet(viewsets.ModelViewSet):
    """
    巡检计划 CRUD 操作 ViewSet
    """
    permission_classes = [permissions.IsNetworkEngineer]
    queryset = PatrolPlan.objects.all()
    serializer_class = PatrolPlanSerializer
    pagination_class = CustomPagination

    # 添加过滤后端
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    # 可过滤字段
    filterset_fields = ['publisher', 'executor']
    # 可搜索字段
    search_fields = ['plan_name', 'patrol_content']
    # 可排序字段
    ordering_fields = ['start_time', 'end_time', 'created_at', 'updated_at']
    ordering = ['-created_at']  # 默认按创建时间倒序

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


class PatrolTaskViewSet(viewsets.ModelViewSet):
    """
    计划任务 CRUD 操作 ViewSet
    """
    permission_classes = [permissions.IsNetworkEngineer]
    queryset = PatrolTask.objects.all()
    serializer_class = PatrolTaskSerializer
    pagination_class = CustomPagination

    # 添加过滤后端
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    # 可过滤字段
    filterset_fields = ['publisher', 'executor']
    # 可搜索字段
    search_fields = ['task_name', 'task_content']
    # 可排序字段
    ordering_fields = ['start_time', 'end_time', 'created_at', 'updated_at']
    ordering = ['-created_at']  # 默认按创建时间倒序

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
