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

ipv4_validator = RegexValidator(
    regex=r'^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$',
    message="请输入有效的 IPv4 地址，如 192.168.1.1"
)
login_protocol_validator = RegexValidator(
    regex=r'^(ssh|telnet|http|https)$',
    message="登录协议必须是 'ssh' 或 'telnet'"
)

device_type_validator = RegexValidator(
    regex=r'^(交换机|路由器|防火墙|无线AP|服务器|其他)$',
    message="设备类型必须是：交换机、路由器、防火墙、无线AP、服务器、其他"
)


class NetworkDevice(models.Model):
    id = models.AutoField(primary_key=True)
    device_name = models.CharField(null=True, max_length=255, verbose_name='设备名称')
    ip_address = models.GenericIPAddressField(
        validators=[ipv4_validator],
        null=True,
        help_text="管理IP地址（可为空，支持IPv4/IPv6）"
    )
    mac_address = models.CharField(
        max_length=17,
        null=True,
        validators=[RegexValidator(regex=r'^([0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}$')],
        help_text="MAC地址"
    )
    type = models.CharField(max_length=64, default="交换机", help_text="设备类型")
    model = models.CharField(max_length=64, null=True, blank=True, help_text="设备型号")
    sn = models.CharField(max_length=64, null=True, blank=True, help_text="序列号")
    location = models.CharField(max_length=255, null=True, blank=True, help_text="物理位置，如 3楼机房A排")
    maintenance_start = models.DateField(blank=True, null=True, help_text="维保开始日期")
    maintenance_end = models.DateField(blank=True, null=True, help_text="维保截止日期")
    local_admin_name = models.CharField(max_length=64, blank=True, null=True, help_text="本地管理员用户名")
    local_admin_password = models.CharField(max_length=128, blank=True, null=True,
                                            help_text="本地管理员密码（建议加密存储）")
    system_info = models.CharField(max_length=255, null=True, help_text="系统信息，如操作系统、版本、架构等")
    # === 登录管理协议配置（用于自动化采集，非必填）===
    login_protocol = models.CharField(max_length=6, default="ssh", validators=[login_protocol_validator],
                                      help_text="远程登录协议是telnet还是ssh")
    login_username = models.CharField(max_length=64, null=True, blank=True, help_text="登录用户名")
    login_password = models.CharField(max_length=128, null=True, blank=True, help_text="登录密码")
    login_port = models.IntegerField(default=22, help_text="端口号")

    is_active = models.BooleanField(
        default=True,
        help_text="是否在使用中"
    )
    # === 时间戳 ===
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "网络设备"
        verbose_name_plural = "网络设备"
        ordering = ['-updated_at']


class IPAM(models.Model):
    """
    IP网段管理
    """
    id = models.AutoField(primary_key=True, verbose_name='IP地址管理id')
    ip_address = models.CharField(max_length=255, verbose_name='IP地址段')
    dhcp = models.CharField(max_length=255, verbose_name='DHCP地址段')
    reserved = models.CharField(max_length=255, verbose_name='保留地址段')
    vlan = models.CharField(max_length=4, verbose_name='VLAN接口')
    business_system = models.CharField(max_length=255, verbose_name='承载业务')
    remarks = models.TextField(null=True, verbose_name='备注')


class Terminal(models.Model):
    """
    办公终端信息
    """
    id = models.AutoField(primary_key=True, verbose_name='终端信息id')
    name = models.CharField(max_length=255, verbose_name='终端名称')
    ip_address = models.CharField(max_length=255, verbose_name='IP地址')
    mac_address = models.CharField(max_length=255, verbose_name='MAC地址')
    vlan = models.CharField(max_length=255, null=True, blank=True, verbose_name='VLAN')
    remarks = models.TextField(null=True, verbose_name='备注')
