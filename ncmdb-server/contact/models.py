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
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(regex=r'^[\d\-\*\s]+$', message="请输入有效的电话号码")


class Contact(models.Model):
    """外部联系人"""
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name='姓名')
    sex = models.CharField(default='男', max_length=1, verbose_name='性别，默认男')
    phone1 = models.CharField(max_length=20, validators=[phone_validator], verbose_name='电话 1')
    phone2 = models.CharField(max_length=20, validators=[phone_validator], null=True, blank=True, verbose_name='电话 2')
    email = models.EmailField(null=True, verbose_name='邮箱')
    company = models.CharField(max_length=100, null=True, verbose_name='公司')
    position = models.CharField(max_length=100, null=True, verbose_name='职务')
    address = models.CharField(max_length=200, null=True, verbose_name='地址')
    remarks = models.TextField(null=True, verbose_name='备注')

    class Meta:
        verbose_name = '联系人'
        verbose_name_plural = '联系人'
        ordering = ['name']
