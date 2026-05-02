/*
 * Copyright 2026 dingtongbin
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */
<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { getWorkOrderDetail, submitEvaluation } from '../api/api.js'
import { formatTimeAgo } from '../utils/timeFormat.js'

const route = useRoute()
const router = useRouter()

// 工单详情数据
const workOrder = ref(null)
const loading = ref(false)

// 评价表单
const evaluationForm = ref({
  satisfaction: 5,
  content: ''
})
const showEvaluationDialog = ref(false)
const submitLoading = ref(false)

// 状态步骤定义
const statusSteps = [
  { key: 'pending', title: '提交工单', nextTitle: '已受理', nextDesc: '待受理' },
  { key: 'accepted', title: '已受理', nextTitle: '处理中', nextDesc: '待处理' },
  { key: 'processing', title: '处理中', nextTitle: '已完成', nextDesc: '待完成' },
  { key: 'completed', title: '已完成', nextTitle: null, nextDesc: null }
]

// 计算当前应该显示哪些步骤
const visibleSteps = computed(() => {
  if (!workOrder.value) return []

  const currentIndex = statusSteps.findIndex(step => step.key === workOrder.value.status)
  // 显示当前状态和下一个待处理状态
  const visibleCount = currentIndex < statusSteps.length - 1 ? currentIndex + 2 : currentIndex + 1

  return statusSteps.slice(0, visibleCount).map((step, index) => {
    const stepIndex = statusSteps.indexOf(step)
    const isCompleted = stepIndex < currentIndex
    const isCurrent = stepIndex === currentIndex
    const isNext = stepIndex === currentIndex + 1

    // 获取时间
    let timestamp = ''
    let description = ''

    if (step.key === 'pending') {
      timestamp = workOrder.value.created_at ? new Date(workOrder.value.created_at).toLocaleString('zh-CN') : ''
      description = formatTimeAgo(workOrder.value.created_at)
    } else if (step.key === 'accepted' && workOrder.value.accepted_at) {
      timestamp = new Date(workOrder.value.accepted_at).toLocaleString('zh-CN')
      description = formatTimeAgo(workOrder.value.accepted_at)
    } else if (step.key === 'processing') {
      description = isCurrent ? '正在处理' : ''
    } else if (step.key === 'completed' && workOrder.value.completed_at) {
      timestamp = new Date(workOrder.value.completed_at).toLocaleString('zh-CN')
      description = formatTimeAgo(workOrder.value.completed_at)
    }

    // 如果是下一个待处理状态
    if (isNext && !isCompleted && !isCurrent) {
      description = step.nextDesc
    }

    return {
      ...step,
      completed: isCompleted,
      current: isCurrent,
      next: isNext,
      timestamp,
      description: description || step.nextDesc
    }
  })
})

// 获取状态文本
const getStatusText = (status) => {
  const statusMap = {
    'pending': '待受理',
    'accepted': '已受理',
    'processing': '处理中',
    'resolved': '已解决',
    'completed': '已完成'
  }
  return statusMap[status] || '未知'
}

// 获取状态类型
const getStatusType = (status) => {
  const typeMap = {
    'pending': 'info',
    'accepted': 'warning',
    'processing': 'primary',
    'resolved': 'success',
    'completed': 'success'
  }
  return typeMap[status] || 'info'
}

// 获取紧急程度文本
const getLevelText = (level) => {
  const levelMap = {
    'low': '低',
    'normal': '一般',
    'high': '高',
    'urgent': '紧急'
  }
  return levelMap[level] || '一般'
}

// 获取紧急程度标签类型
const getLevelType = (level) => {
  const typeMap = {
    'low': 'info',
    'normal': '',
    'high': 'warning',
    'urgent': 'danger'
  }
  return typeMap[level] || ''
}

// 加载工单详情
const loadWorkOrderDetail = async () => {
  loading.value = true
  try {
    const data = await getWorkOrderDetail(route.params.id)
    workOrder.value = data

    // 如果已完成且未评价，显示评价对话框
    if (data.status === 'completed' && !data.has_evaluated) {
      showEvaluationDialog.value = true
    }
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载工单详情失败')
  } finally {
    loading.value = false
  }
}

// 提交评价
const handleSubmitEvaluation = async () => {
  if (!evaluationForm.value.satisfaction) {
    ElMessage.warning('请选择满意度')
    return
  }

  submitLoading.value = true
  try {
    const result = await submitEvaluation(route.params.id, {
      satisfaction: evaluationForm.value.satisfaction,
      content: evaluationForm.value.content
    })

    if (result.success) {
      ElMessage.success('评价提交成功')
      showEvaluationDialog.value = false
      loadWorkOrderDetail()
    } else {
      ElMessage.error(result.error || '评价失败')
    }
  } catch (error) {
    console.error('评价失败:', error)
    ElMessage.error('评价提交失败')
  } finally {
    submitLoading.value = false
  }
}

// 返回列表
const goBack = () => {
  router.back()
}

onMounted(() => {
  loadWorkOrderDetail()
})
</script>

<template>
  <div class="detail-container">
    <!-- 返回按钮 -->
    <div class="back-header">
      <el-button @click="goBack" icon="ArrowLeft">返回</el-button>
    </div>

    <div v-loading="loading" class="detail-content">
      <template v-if="workOrder">
        <!-- 工单基本信息卡片 -->
        <div class="info-card">
          <div class="card-header">
            <h2 class="card-title">工单详情</h2>
            <div class="status-tags">
              <el-tag :type="getLevelType(workOrder.level)" size="small">
                {{ getLevelText(workOrder.level) }}
              </el-tag>
              <el-tag :type="getStatusType(workOrder.status)" size="small">
                {{ getStatusText(workOrder.status) }}
              </el-tag>
            </div>
          </div>

          <el-descriptions :column="1" border>
            <el-descriptions-item label="工单编号">
              {{ workOrder.work_order_no }}
            </el-descriptions-item>
            <el-descriptions-item label="报修人">
              {{ workOrder.name }} ({{ workOrder.username }})
            </el-descriptions-item>
            <el-descriptions-item label="联系电话" v-if="workOrder.phone">
              <a :href="`tel:${workOrder.phone}`" class="phone-link">
                {{ workOrder.phone }}
              </a>
            </el-descriptions-item>
            <el-descriptions-item label="故障地点">
              {{ workOrder.location }}
            </el-descriptions-item>
            <el-descriptions-item label="故障描述">
              {{ workOrder.description }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">
              {{ new Date(workOrder.created_at).toLocaleString('zh-CN') }}
            </el-descriptions-item>
            <el-descriptions-item label="处理结果" v-if="workOrder.result">
              {{ workOrder.result }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 处理进度 - 简化版时间树 -->
        <div class="timeline-card">
          <h3 class="card-title">处理进度</h3>
          <div class="timeline-simple">
            <div
                v-for="(step, index) in visibleSteps"
                :key="index"
                class="timeline-item"
                :class="{
                'is-completed': step.completed,
                'is-current': step.current,
                'is-next': step.next
              }"
            >
              <div class="timeline-node">
                <div class="timeline-dot" :class="{
                  'dot-primary': step.current,
                  'dot-success': step.completed,
                  'dot-default': step.next
                }"></div>
                <div v-if="index < visibleSteps.length - 1" class="timeline-line" :class="{
                  'line-success': step.completed,
                  'line-default': !step.completed
                }"></div>
              </div>
              <div class="timeline-content">
                <div class="timeline-header">
                  <span class="timeline-title">{{ step.title }}</span>
                  <span v-if="step.timestamp" class="timeline-time">{{ step.timestamp }}</span>
                </div>
                <p class="timeline-desc">{{ step.description }}</p>
                <p v-if="step.next" class="timeline-waiting">等待：{{ step.nextTitle }}</p>
              </div>
            </div>
          </div>
        </div>

        <!-- 处理记录（如果有） -->
        <div class="logs-card" v-if="workOrder.handle_logs && workOrder.handle_logs.length > 0">
          <h3 class="card-title">处理记录</h3>
          <div class="logs-list">
            <div
                v-for="log in workOrder.handle_logs"
                :key="log.id"
                class="log-item"
            >
              <div class="log-header">
                <span class="log-type">{{ log.handle_type }}</span>
                <span class="log-time">{{ new Date(log.handle_at).toLocaleString('zh-CN') }}</span>
              </div>
              <p class="log-content">{{ log.content }}</p>
              <div class="log-footer">
                <span class="log-handler">处理人：{{ log.handler_name }}</span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </div>

    <!-- 评价对话框 -->
    <el-dialog
        v-model="showEvaluationDialog"
        title="工单评价"
        width="90%"
        :close-on-click-modal="false"
    >
      <div class="evaluation-form">
        <p class="evaluation-title">请对本次服务进行评价</p>

        <el-rate
            v-model="evaluationForm.satisfaction"
            :texts="['非常不满意', '不满意', '一般', '满意', '非常满意']"
            show-text
            style="margin: 20px 0"
        />

        <el-input
            v-model="evaluationForm.content"
            type="textarea"
            :rows="4"
            placeholder="请输入评价内容（选填）"
            maxlength="500"
            show-word-limit
        />
      </div>

      <template #footer>
        <el-button @click="showEvaluationDialog = false">取消</el-button>
        <el-button type="primary" @click="handleSubmitEvaluation" :loading="submitLoading">
          提交评价
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.detail-container {
  width: 100%;
  height: 100%;
  background-color: #f5f7fa;
  overflow-y: auto;
  -webkit-overflow-scrolling: touch;
}

.back-header {
  padding: 10px 15px;
  background: white;
  border-bottom: 1px solid #e6e6e6;
  position: sticky;
  top: 0;
  z-index: 100;
}

.detail-content {
  padding: 15px;
}

.info-card, .timeline-card, .logs-card {
  background: white;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
}

.card-title {
  margin: 0 0 15px 0;
  font-size: 18px;
  font-weight: 600;
  color: #333;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.status-tags {
  display: flex;
  gap: 8px;
}

.phone-link {
  color: #409EFF;
  text-decoration: none;
}

/* 简化版时间树样式 */
.timeline-simple {
  padding: 10px 0;
}

.timeline-item {
  display: flex;
  gap: 12px;
  padding-bottom: 20px;
  position: relative;
}

.timeline-item:last-child {
  padding-bottom: 0;
}

.timeline-node {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.timeline-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  margin-top: 4px;
  flex-shrink: 0;
}

.dot-primary {
  background: #409EFF;
  box-shadow: 0 0 0 3px rgba(64, 158, 255, 0.2);
}

.dot-success {
  background: #67C23A;
}

.dot-default {
  background: #DCDFE6;
}

.timeline-line {
  width: 2px;
  flex-grow: 1;
  margin-top: 8px;
  min-height: 40px;
}

.line-success {
  background: #67C23A;
}

.line-default {
  background: #DCDFE6;
}

.timeline-content {
  flex: 1;
  min-width: 0;
}

.timeline-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.timeline-title {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}

.timeline-time {
  font-size: 12px;
  color: #999;
}

.timeline-desc {
  margin: 0;
  font-size: 13px;
  color: #666;
  line-height: 1.5;
}

.timeline-waiting {
  margin: 6px 0 0 0;
  font-size: 12px;
  color: #909399;
  font-style: italic;
}

/* 处理记录样式 */
.logs-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.log-item {
  padding: 12px;
  background: #fafafa;
  border-radius: 6px;
  border-left: 3px solid #E6A23C;
}

.log-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.log-type {
  padding: 2px 8px;
  background: #ECF5FF;
  color: #409EFF;
  border-radius: 4px;
  font-size: 12px;
}

.log-time {
  font-size: 12px;
  color: #999;
}

.log-content {
  margin: 0 0 8px 0;
  font-size: 14px;
  color: #333;
  line-height: 1.6;
  word-break: break-all;
}

.log-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.log-handler {
  font-size: 13px;
  color: #666;
}

/* 评价表单样式 */
.evaluation-form {
  padding: 10px;
}

.evaluation-title {
  font-size: 16px;
  color: #333;
  margin: 0 0 15px 0;
  text-align: center;
}

/* 媒体查询 - 移动端优化 */
@media (max-width: 768px) {
  .detail-content {
    padding: 10px;
  }

  .info-card, .timeline-card, .logs-card {
    padding: 12px;
    border-radius: 6px;
  }

  .card-title {
    font-size: 16px;
  }

  .card-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }

  :deep(.el-descriptions__label) {
    font-size: 13px;
    padding: 8px 10px;
  }

  :deep(.el-descriptions__content) {
    font-size: 14px;
    padding: 8px 10px;
  }

  .timeline-title {
    font-size: 14px;
  }

  .timeline-desc {
    font-size: 12px;
  }

  .timeline-time {
    font-size: 11px;
  }

  .log-content {
    font-size: 13px;
  }
}

/* 小屏幕进一步优化 */
@media (max-width: 480px) {
  .back-header {
    padding: 8px 10px;
  }

  .detail-content {
    padding: 8px;
  }

  .info-card, .timeline-card, .logs-card {
    padding: 10px;
  }

  .card-title {
    font-size: 15px;
  }

  :deep(.el-descriptions__label) {
    font-size: 12px;
  }

  :deep(.el-descriptions__content) {
    font-size: 13px;
  }

  .timeline-dot {
    width: 10px;
    height: 10px;
  }

  .timeline-title {
    font-size: 13px;
  }

  .timeline-desc {
    font-size: 11px;
  }
}
</style>
