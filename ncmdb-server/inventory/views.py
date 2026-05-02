from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from inventory.models import InventoryItem, InventoryRecord
from inventory.serializers import InventoryItemSerializer, InventoryRecordSerializer
from user import permissions


class CustomPagination(PageNumberPagination):
    page_size = 50
    page_size_query_param = 'page_size'
    max_page_size = 100


class InventoryItemModelViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsNetworkEngineer]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'item_type', 'features', 'location', 'remarks']

    @action(detail=False, methods=['post'], url_path='bulk-delete')
    def bulk_delete(self, request):
        """
        通用批量删除方法，支持任意主键字段
        """
        ids = request.data.get('ids', [])
        if not ids:
            return Response({'error': '请选择要删除的记录'}, status=status.HTTP_400_BAD_REQUEST)

        # 获取模型类和主键字段名
        model_class = self.queryset.model
        primary_key_field = model_class._meta.pk.name

        # 构造查询条件
        filter_kwargs = {f'{primary_key_field}__in': ids}
        deleted_count, _ = model_class.objects.filter(**filter_kwargs).delete()

        return Response({'message': f'成功删除 {deleted_count} 条记录'}, status=status.HTTP_200_OK)


class InventoryRecordViewSet(viewsets.ModelViewSet):
    queryset = InventoryRecord.objects.all()
    serializer_class = InventoryRecordSerializer
    permission_classes = [permissions.IsNetworkEngineer]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['record_type', 'inventory_item', 'operator']
    search_fields = ['inventory_item__name', 'operator__real_name', 'remarks']
    ordering_fields = ['operation_time', 'quantity']

    @action(detail=False, methods=['get'], url_path='item/(?P<item_id>[^/.]+)/records')
    def get_item_records(self, request, item_id=None):
        """
        获取单个物品的所有出入库记录
        """
        try:
            item = InventoryItem.objects.get(pk=item_id)
        except InventoryItem.DoesNotExist:
            return Response({'error': '物品不存在'}, status=status.HTTP_404_NOT_FOUND)

        records = InventoryRecord.objects.filter(inventory_item=item).order_by('-operation_time')
        page = self.paginate_queryset(records)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(records, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['post'], url_path='item/(?P<item_id>[^/.]+)/operate')
    def operate_item(self, request, item_id=None):
        """
        对单个物品进行出入库操作
        """
        # 获取物品
        try:
            item = InventoryItem.objects.get(pk=item_id)
        except InventoryItem.DoesNotExist:
            return Response({'error': '物品不存在'}, status=status.HTTP_404_NOT_FOUND)
        # 构造数据
        data = {'inventory_item': item.id,
            'record_type': request.data.get('record_type') or request.data.get('operation_type'),
            'quantity': request.data.get('quantity'), 'operator': request.user.id,
            'remarks': request.data.get('remarks', '')}
        # 序列化器校验
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response({'error': '数据验证失败', 'details': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        # 检查库存
        if data['record_type'] == 'out' and item.quantity < data['quantity']:
            return Response({'error': f'库存不足，当前库存为 {item.quantity}'}, status=status.HTTP_400_BAD_REQUEST)
        # 保存记录
        serializer.save()
        # 更新库存
        if data['record_type'] == 'in':
            item.quantity = F('quantity') + data['quantity']
        else:
            item.quantity = F('quantity') - data['quantity']
        item.save()

        item.refresh_from_db()

        return Response({'message': '操作成功', 'current_quantity': item.quantity, 'record': serializer.data},
            status=status.HTTP_201_CREATED)
