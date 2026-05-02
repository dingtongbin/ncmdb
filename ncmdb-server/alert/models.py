from django.db import models


class Alert(models.Model):
    """
    告警模型
    """
    # 基本信息
    source = models.CharField(max_length=50, default='other', verbose_name='告警来源')
    severity = models.CharField(max_length=20, default='warning', verbose_name='告警级别')
    status = models.CharField(max_length=20, default='未确认', verbose_name='告警状态')
    # 告警内容
    title = models.CharField(max_length=200, default='snmp告警', verbose_name='告警标题')
    description = models.TextField(blank=True, null=True, verbose_name='告警详情')
    # 标识信息
    host = models.CharField(max_length=100, blank=True, null=True, verbose_name='主机名')
    ip = models.CharField(max_length=100, blank=True, null=True, verbose_name='IP地址')
    # 原始数据
    raw_data = models.JSONField(default=dict, blank=True, null=True, verbose_name='原始数据')
    # 时间戳
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    confirm_at = models.DateTimeField(auto_now_add=True, verbose_name='确认时间')

    class Meta:
        db_table = 'alerts'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.source})"


class WebhookReceiver(models.Model):
    """
    Webhook接收配置模型
    """

    name = models.CharField(max_length=100, unique=True, verbose_name='名称')
    source = models.CharField(max_length=50, default="zabbix", verbose_name='来源平台')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    api_token = models.CharField(max_length=200, verbose_name='密钥令牌')
    remarks = models.TextField(blank=True, null=True, verbose_name='备注')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')

    class Meta:
        db_table = 'webhook_receivers'
        verbose_name = 'Webhook接收器'
        ordering = ['-updated_at']
        verbose_name_plural = 'Webhook接收器'

    def __str__(self):
        return self.name
