from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from contact.models import Contact
from contact.serializers import ContactSerializer
from user import permissions


class CustomPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 100


class ContactModelViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    permission_classes = [permissions.IsNetworkEngineer]
    pagination_class = CustomPagination
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['name', 'phone1', 'phone2', 'company', 'address', 'remarks']

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
