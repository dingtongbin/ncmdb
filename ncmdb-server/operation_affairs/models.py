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
# models.py

from django.db import models


class PatrolPlan(models.Model):
    """巡检计划"""
    plan_name = models.CharField(max_length=100, verbose_name='巡检计划名称')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    publisher = models.CharField(max_length=100, verbose_name='发布人')
    executor = models.CharField(max_length=100, verbose_name='执行人')
    patrol_content = models.TextField(verbose_name='巡检内容')
    output_content = models.TextField(verbose_name='巡检输出内容')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '巡检计划'
        verbose_name_plural = '巡检计划'


class PatrolTask(models.Model):
    """计划任务"""
    task_name = models.CharField(max_length=100, verbose_name='计划任务名称')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    publisher = models.CharField(max_length=100, verbose_name='发布人')
    executor = models.CharField(max_length=100, verbose_name='执行人')
    task_content = models.TextField(verbose_name='任务内容')
    task_target = models.TextField(verbose_name='任务目标')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '巡检任务'
        verbose_name_plural = '巡检任务'
