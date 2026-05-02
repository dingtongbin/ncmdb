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
from django.db import models
from django.utils import timezone


class InventoryItem(models.Model):
    """库存物品"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='物品名称')
    item_type = models.CharField(max_length=20, verbose_name='物品类型')
    image = models.CharField(max_length=255, null=True, verbose_name='物品图片')
    location = models.CharField(max_length=200, verbose_name='存放位置')
    quantity = models.IntegerField(default=0, verbose_name='当前库存')
    unit = models.CharField(max_length=20, verbose_name='单位')
    created_at = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='更新时间')
    remarks = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '库存物品'
        verbose_name_plural = '库存物品'
        ordering = ['-created_at']


class InventoryRecord(models.Model):
    """物品出入库记录"""
    RECORD_TYPE_CHOICES = [
        ('in', '入库'),
        ('out', '出库'),
    ]

    id = models.AutoField(primary_key=True)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, verbose_name='物品')
    record_type = models.CharField(max_length=3, choices=RECORD_TYPE_CHOICES, verbose_name='操作类型')
    quantity = models.IntegerField(verbose_name='数量')
    operator = models.ForeignKey('user.User', on_delete=models.PROTECT, verbose_name='操作人')
    operation_time = models.DateTimeField(default=timezone.now, verbose_name='操作时间')
    remarks = models.TextField(blank=True, verbose_name='备注')

    class Meta:
        verbose_name = '出入库记录'
        verbose_name_plural = '出入库记录'
        ordering = ['-operation_time']
