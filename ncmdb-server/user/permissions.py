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
from rest_framework.permissions import BasePermission


class IsNetworkEngineer(BasePermission):
    """
    网络工程师权限类
    只允许纯网络工程师访问（is_network_engineer=True 且 is_staff=False 且 is_superuser=False）
    如果同时具有管理员或超级用户权限，则返回False
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_engineer = getattr(request.user, 'is_network_engineer', False)
        is_admin = request.user.is_staff or request.user.is_superuser

        # 必须只是网工，不能同时是管理员
        return is_engineer and not is_admin


class IsNormalUser(BasePermission):
    """
    普通用户权限类
    只允许既不是网工也不是管理员的普通用户访问
    如果具有网工或管理员任一权限，则返回False
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_engineer = getattr(request.user, 'is_network_engineer', False)
        is_admin = request.user.is_staff or request.user.is_superuser

        # 普通用户不能有任何特殊权限
        return not is_engineer and not is_admin


class IsAdminOrSuperuser(BasePermission):
    """
    管理员或超级用户权限类
    只允许纯管理员访问（is_staff=True 或 is_superuser=True）
    如果同时具有网工权限，则返回False
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        is_engineer = getattr(request.user, 'is_network_engineer', False)
        is_admin = request.user.is_staff or request.user.is_superuser

        # 必须是管理员，且不能是网工
        return is_admin and not is_engineer
