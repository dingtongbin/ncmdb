from django.db import models


class EquipmentRooms(models.Model):
    """设备间基本信息"""
    id = models.AutoField(primary_key=True, verbose_name="设备间id")
    name = models.CharField(max_length=255, verbose_name='设备间名称')
    location = models.CharField(max_length=255, null=True, blank=True, default='无', verbose_name='地址')
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '机房'
        verbose_name_plural = '机房管理'


class Rack(models.Model):
    """机柜信息"""

    equipment_room_id = models.BigIntegerField(verbose_name='所属设备间id', default=0)
    id = models.AutoField(primary_key=True, verbose_name="机柜 id")
    name = models.CharField(max_length=255, verbose_name='机柜名称')
    height = models.IntegerField(verbose_name='高度 (U)')
    width = models.IntegerField(verbose_name='宽度 (mm)', default=600)
    depth = models.IntegerField(verbose_name='深度 (mm)', default=1000)
    remarks = models.TextField(null=True, blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '机柜'
        verbose_name_plural = '机柜管理'


class InfrastructureEquipment(models.Model):
    """基础设施设备"""
    rack_id = models.BigIntegerField(verbose_name='所属机柜id', default=0)
    id = models.AutoField(primary_key=True, verbose_name="设备 id")
    name = models.CharField(max_length=100, verbose_name='设备名称')
    image = models.TextField(blank=True, null=True, verbose_name='基础设施设备图片')
    type = models.CharField(max_length=30, verbose_name='设备类型')
    brand = models.CharField(max_length=50, verbose_name='品牌')
    model = models.CharField(max_length=100, verbose_name='型号')
    serial_number = models.CharField(max_length=100, verbose_name='序列号')
    device_number = models.CharField(max_length=50, unique=True, verbose_name='设备编号')
    is_active = models.BooleanField(default=True, verbose_name='是否启用中')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')

    class Meta:
        verbose_name = '基础设施设备'
        verbose_name_plural = '基础设施设备'


class Connection(models.Model):
    """
    基础设施设备连线信息
    """
    device_id = models.BigIntegerField(verbose_name='所属设备id')
    home_interface = models.CharField(max_length=255, verbose_name='本端接口')
    peer_interface = models.CharField(max_length=255, verbose_name='对端接口')
    peer_device = models.CharField(max_length=255, verbose_name='对端设备')
    connection_type = models.CharField(max_length=255, verbose_name='接口连线类型')
    remarks = models.TextField(null=True, verbose_name='备注')
