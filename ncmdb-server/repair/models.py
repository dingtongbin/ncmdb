from django.db import models

from user.models import User


class WorkOrder(models.Model):
    """
    故障报修工单
    """
    # 工单状态选择
    STATUS_CHOICES = [
        ('pending', '待受理'),
        ('accepted', '已受理'),
        ('processing', '处理中'),
        ('resolved', '已解决'),
        ('completed', '已完成'),
    ]

    # 紧急程度选择
    LEVEL_CHOICES = [
        ('low', '低'),
        ('normal', '一般'),
        ('high', '高'),
        ('urgent', '紧急'),
    ]

    # 工单基础信息
    id = models.AutoField(primary_key=True, verbose_name='工单 ID')
    work_order_no = models.CharField(max_length=6, unique=True, editable=False, verbose_name='工单编号')

    # 报修人信息（简化）
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='work_orders',
        verbose_name='报修人'
    )
    # 故障信息（简化）
    location = models.CharField(max_length=200, verbose_name='故障地点')
    description = models.TextField(verbose_name='故障描述')
    level = models.CharField(max_length=10, default='normal', choices=LEVEL_CHOICES, verbose_name='紧急程度')
    # 工单分配
    assignee = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_work_orders',
        verbose_name='处理人'
    )

    # 工单当前状态
    status = models.CharField(
        max_length=20,
        default='pending',
        choices=STATUS_CHOICES,
        verbose_name='当前状态'
    )

    # 处理结果（简化）
    result = models.TextField(blank=True, null=True, verbose_name='处理结果')

    # 时间信息（简化）
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='完成时间')

    class Meta:
        verbose_name = '工单'
        verbose_name_plural = '工单管理'
        ordering = ['-created_at']
        db_table = 'repair_work_order'

    def __str__(self):
        user_str = f"{self.user.username} ({self.user.real_name})" if self.user else "未知用户"
        return f"工单{self.work_order_no} - {user_str}"

    @classmethod
    def generate_work_order_no(cls):
        """生成 6 位纯数字工单编号"""
        # 使用自增 ID 作为工单编号，不足 6 位前面补 0
        if cls.objects.count() == 0:
            return '000001'
        last_order = cls.objects.order_by('-id').first()
        if last_order:
            next_id = last_order.id + 1
        else:
            next_id = 1
        return str(next_id).zfill(6)

    def save(self, *args, **kwargs):
        if not self.work_order_no:
            self.work_order_no = self.generate_work_order_no()
        super().save(*args, **kwargs)


class WorkOrderHandleLog(models.Model):
    """
    工单处理记录表（简化版）
    """
    HANDLE_TYPE_CHOICES = [
        ('diagnose', '诊断'),
        ('repair', '维修'),
        ('configure', '配置'),
        ('other', '其他'),
    ]

    id = models.AutoField(primary_key=True, verbose_name='记录 ID')
    work_order = models.ForeignKey(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='handle_logs',
        verbose_name='工单'
    )

    # 处理人（简化）
    handler = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='处理人'
    )

    # 处理信息（简化）
    handle_type = models.CharField(
        max_length=20,
        choices=HANDLE_TYPE_CHOICES,
        default='other',
        verbose_name='处理类型'
    )
    content = models.TextField(verbose_name='处理内容')

    # 时间
    handle_at = models.DateTimeField(auto_now_add=True, verbose_name='处理时间')

    class Meta:
        verbose_name = '工单处理记录'
        verbose_name_plural = '工单处理记录'
        ordering = ['-handle_at']
        db_table = 'repair_work_order_handle_log'

    def __str__(self):
        handler_name = self.handler.real_name if self.handler else "未知"
        return f"工单{self.work_order.work_order_no} - {handler_name}"


class WorkOrderEvaluation(models.Model):
    """
    工单评价表（简化版）
    """
    SATISFACTION_CHOICES = [
        (1, '非常不满意'),
        (2, '不满意'),
        (3, '一般'),
        (4, '满意'),
        (5, '非常满意'),
    ]

    id = models.AutoField(primary_key=True, verbose_name='评价 ID')
    work_order = models.OneToOneField(
        WorkOrder,
        on_delete=models.CASCADE,
        related_name='evaluation',
        verbose_name='工单'
    )

    # 评分（简化）
    satisfaction = models.IntegerField(
        choices=SATISFACTION_CHOICES,
        verbose_name='满意度'
    )

    # 评价内容（简化）
    content = models.CharField(max_length=255, blank=True, null=True, verbose_name='评价内容')

    # 时间
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='评价时间')

    class Meta:
        verbose_name = '工单评价'
        verbose_name_plural = '工单评价'
        ordering = ['-created_at']
        db_table = 'repair_work_order_evaluation'

    def __str__(self):
        return f"工单{self.work_order.work_order_no} - 满意度{self.satisfaction}"
