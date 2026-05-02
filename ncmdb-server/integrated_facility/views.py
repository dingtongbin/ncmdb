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
import logging

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from integrated_facility.models import EquipmentRooms, InfrastructureEquipment, Rack, Connection
from integrated_facility.serializers import EquipmentRoomsSerializer, InfrastructureEquipmentSerializer, RackSerializer, \
    ConnectionSerializer
from user import permissions

logger = logging.getLogger(__name__)


class CustomPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 500


class BaseModelViewSet(viewsets.ModelViewSet):
    """
    基础 ModelViewSet，提供通用功能
    """
    pagination_class = CustomPagination
    permission_classes = [permissions.IsNetworkEngineer]

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    ordering_fields = '__all__'
    ordering = ['id']

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

        model_class = self.queryset.model
        primary_key_field = model_class._meta.pk.name
        filter_kwargs = {f'{primary_key_field}__in': ids}
        deleted_count, _ = model_class.objects.filter(**filter_kwargs).delete()

        logger.info(f"批量删除成功：删除了 {deleted_count} 条记录，IDs: {ids}")

        return Response(
            {'message': f'成功删除 {deleted_count} 条记录'},
            status=status.HTTP_200_OK
        )


class EquipmentRoomsViewSet(BaseModelViewSet):
    """
    设备间 CRUD 操作 ViewSet
    """
    queryset = EquipmentRooms.objects.all()
    serializer_class = EquipmentRoomsSerializer
    search_fields = ['name', 'location', 'remarks']


class RackViewSet(BaseModelViewSet):
    """
    机柜 CRUD 操作 ViewSet
    """
    queryset = Rack.objects.all()
    serializer_class = RackSerializer
    search_fields = ['equipment_room_id', 'name', 'code', 'height', 'width', 'depth', 'remarks']
    filterset_fields = ['equipment_room_id']  # 添加这个以支持按设备间 ID 过滤


class InfrastructureEquipmentViewSet(BaseModelViewSet):
    """
    基础设施设备 CRUD 操作 ViewSet
    """
    queryset = InfrastructureEquipment.objects.all()
    serializer_class = InfrastructureEquipmentSerializer
    search_fields = ['name', 'rack', 'type', 'brand', 'model', 'serial_number', 'device_number', 'is_active', 'remarks']
    filterset_fields = ['rack_id']  # 添加这个以支持按机柜 ID 过滤


class ConnectionViewSet(BaseModelViewSet):
    """
    连接信息 CRUD 操作 ViewSet
    """
    queryset = Connection.objects.all()
    serializer_class = ConnectionSerializer
    search_fields = ['device_id', 'home_interface', 'peer_interface', 'peer_device', 'connection_type', 'remarks']
    filterset_fields = ['device_id']  # 添加这个以支持按设备 ID 过滤
