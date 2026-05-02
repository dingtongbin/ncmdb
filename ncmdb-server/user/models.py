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
# Create your models here.
# app/models/user_model.py
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, username, real_name, password=None, **extra_fields):
        if not username:
            raise ValueError('用户名是必需的')
        if not real_name:
            raise ValueError('用户真实姓名是必需的')
        user = self.model(username=username, real_name=real_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, real_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('超级用户必须设置is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('超级用户必须设置is_superuser=True')

        return self.create_user(username, real_name, password, **extra_fields)


# app/models/user_model.py
class User(AbstractBaseUser, PermissionsMixin):
    # 在 User 类中添加 id 字段
    id = models.AutoField(primary_key=True, verbose_name='ID')

    username = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='工号'
    )

    # 用户真实姓名
    real_name = models.CharField(
        max_length=100,
        verbose_name='真实姓名'
    )

    # 电话号码
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name='电话号码'
    )

    # 部门字段
    department = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='部门'
    )

    # 权限相关字段
    is_staff = models.BooleanField(
        default=False,
        verbose_name='职员状态',
        help_text='指明用户是否可以登录到管理站点。'
    )
    is_network_engineer = models.BooleanField(
        default=False,
        verbose_name='网络管理员',
        help_text='指明用户是否为网络工程师角色。'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='激活状态',
        help_text='指明用户是否被认为是活跃的。以非活跃用户身份登录应被禁止。'
    )

    # 使用自定义管理器
    objects = UserManager()

    # 设置认证字段
    USERNAME_FIELD = 'username'

    # 创建超级用户时必需的字段
    REQUIRED_FIELDS = ['real_name', 'phone', 'department']

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户管理'
        db_table = 'auth_user'

    def __str__(self):
        return f"{self.username} ({self.real_name})"

    def get_full_name(self):
        return self.real_name

    def get_short_name(self):
        return self.real_name
