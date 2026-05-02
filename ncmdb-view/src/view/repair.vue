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
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Refresh } from '@element-plus/icons-vue'
import {acceptWorkOrder, getEngineerWorkOrders, submitWorkOrderResult} from "../api/repair_api.js";


// 搜索表单
const searchForm = reactive({
  status: '',
  level: '',
  keyword: ''
})

// 分页配置
const pagination = reactive({
  page: 1,
  page_size: 50,
  total: 0
})

// 工单列表
const workOrderList = ref([])
const loading = ref(false)

// 抽屉相关
const drawerVisible = ref(false)
const currentWorkOrder = ref(null)
const submitLoading = ref(false)

// 处理结果表单
const resultFormRef = ref(null)
const resultForm = reactive({
  handle_type: 'repair',
  content: '',
  result: ''
})

// 表单验证规则
const resultRules = {
  handle_type: [
    { required: true, message: '请选择处理类型', trigger: 'change' }
  ],
  result: [
    { required: true, message: '请填写处理结果', trigger: 'blur' }
  ]
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

// 获取状态标签类型
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

// 加载工单列表
const loadWorkOrders = async () => {
  loading.value = true
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      ...searchForm
    }

    const data = await getEngineerWorkOrders(params)
    workOrderList.value = data.results
    pagination.total = data.count
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载工单列表失败')
  } finally {
    loading.value = false
  }
}

// 搜索
const handleSearch = () => {
  pagination.page = 1
  loadWorkOrders()
}

// 重置
const handleReset = () => {
  searchForm.status = ''
  searchForm.level = ''
  searchForm.keyword = ''
  pagination.page = 1
  loadWorkOrders()
}

// 分页变化
const handleSizeChange = () => {
  loadWorkOrders()
}

const handlePageChange = () => {
  loadWorkOrders()
}

// 接单
const handleAccept = async (row) => {
  try {
    await ElMessageBox.confirm(
        `确认接单工单 ${row.work_order_no} 吗？`,
        '接单确认',
        {
          confirmButtonText: '确认',
          cancelButtonText: '取消',
          type: 'warning'
        }
    )

    const result = await acceptWorkOrder(row.id)
    if (result.success) {
      ElMessage.success('接单成功')
      await loadWorkOrders()
    } else {
      ElMessage.error(result.error || '接单失败')
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('接单失败:', error)
      ElMessage.error('接单失败')
    }
  }
}

// 打开提交处理抽屉
const handleSubmitResult = (row) => {
  currentWorkOrder.value = row
  resultForm.handle_type = 'repair'
  resultForm.content = ''
  resultForm.result = ''
  drawerVisible.value = true
}

// 关闭抽屉
const handleDrawerClose = (done) => {
  resultFormRef.value?.resetFields()
  drawerVisible.value = false
  currentWorkOrder.value = null
  if (done) done()
}

// 确认提交处理结果
const handleSubmitResultConfirm = async () => {
  if (!resultFormRef.value) return

  await resultFormRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      const result = await submitWorkOrderResult(currentWorkOrder.value.id, {
        handle_type: resultForm.handle_type,
        content: resultForm.content,
        result: resultForm.result
      })

      if (result.success) {
        ElMessage.success('处理结果提交成功')
        handleDrawerClose()
        loadWorkOrders()
      } else {
        ElMessage.error(result.error || '提交失败')
      }
    } catch (error) {
      console.error('提交失败:', error)
      ElMessage.error('提交失败')
    } finally {
      submitLoading.value = false
    }
  })
}

// 查看详情
const handleViewDetail = (row) => {
  ElMessageBox.alert(
      `<strong>工单编号：</strong>${row.work_order_no}<br>
     <strong>报修人：</strong>${row.name} (${row.username})<br>
     <strong>联系电话：</strong>${row.phone || '无'}<br>
     <strong>故障地点：</strong>${row.location}<br>
     <strong>故障描述：</strong>${row.description}<br>
     <strong>紧急程度：</strong>${row.level_display}<br>
     <strong>当前状态：</strong>${row.status_display}<br>
     <strong>处理人：</strong>${row.assignee_name || '未分配'}<br>
     <strong>创建时间：</strong>${row.created_at}<br>
     ${row.result ? `<strong>处理结果：</strong>${row.result}` : ''}`,
      '工单详情',
      {
        dangerouslyUseHTMLString: true,
        confirmButtonText: '关闭'
      }
  )
}

onMounted(() => {
  loadWorkOrders()
})
</script>

<template>
  <div class="engineer-workorder-container">
    <!-- 搜索筛选栏 -->
    <el-card class="search-card" shadow="never">
      <el-form :inline="true" :model="searchForm" class="search-form">
        <el-form-item label="状态筛选">
          <el-select v-model="searchForm.status" placeholder="全部状态" clearable style="width: 120px">
            <el-option label="待受理" value="pending" />
            <el-option label="已受理" value="accepted" />
            <el-option label="处理中" value="processing" />
            <el-option label="已解决" value="resolved" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>

        <el-form-item label="紧急程度">
          <el-select v-model="searchForm.level" placeholder="全部程度" clearable style="width: 100px">
            <el-option label="低" value="low" />
            <el-option label="一般" value="normal" />
            <el-option label="高" value="high" />
            <el-option label="紧急" value="urgent" />
          </el-select>
        </el-form-item>

        <el-form-item label="关键词">
          <el-input
              v-model="searchForm.keyword"
              placeholder="工单编号/姓名/地点"
              clearable
              style="width: 200px"
              @keyup.enter="handleSearch"
          />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">
            <el-icon><Refresh /></el-icon>
            重置
          </el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <!-- 工单列表表格 -->
    <el-card class="table-card" shadow="never">
      <el-table
          v-loading="loading"
          :data="workOrderList"
          style="width: 100%;height:60vh;"
          border
          stripe
          highlight-current-row
      >
        <el-table-column prop="work_order_no" label="工单编号" width="100" fixed />

        <el-table-column label="报修人信息" width="150">
          <template #default="{ row }">
            <div class="user-info">
              <div class="user-name">{{ row.name }}</div>
              <div class="user-phone">{{ row.phone || '无' }}</div>
            </div>
          </template>
        </el-table-column>

        <el-table-column prop="location" label="故障地点" width="150" show-overflow-tooltip />

        <el-table-column prop="description" label="故障描述" min-width="200" show-overflow-tooltip />

        <el-table-column label="紧急程度" width="100">
          <template #default="{ row }">
            <el-tag :type="getLevelType(row.level)" size="small">
              {{ row.level_display }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="工单状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)" size="small">
              {{ row.status_display }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column prop="created_at" label="创建时间" width="160" />

        <el-table-column label="处理人" width="100">
          <template #default="{ row }">
            {{ row.assignee_name || '未分配' }}
          </template>
        </el-table-column>

        <!-- 固定操作栏 -->
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <div class="action-buttons">
              <!-- 待受理状态：显示接单按钮 -->
              <el-button
                  v-if="row.status === 'pending'"
                  type="primary"
                  size="small"
                  @click="handleAccept(row)"
              >
                接单
              </el-button>

              <!-- 已受理/处理中状态：显示提交处理按钮 -->
              <el-button
                  v-else-if="['accepted', 'processing'].includes(row.status)"
                  type="success"
                  size="small"
                  @click="handleSubmitResult(row)"
              >
                提交处理
              </el-button>

              <!-- 其他状态：查看详情 -->
              <el-button
                  v-else
                  type="info"
                  size="small"
                  @click="handleViewDetail(row)"
              >
                查看
              </el-button>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :total="pagination.total"
          :page-sizes="[50, 100, 200, 500]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
          style="margin-top: 20px; justify-content: flex-end"
      />
    </el-card>

    <!-- 提交处理结果抽屉 -->
    <el-drawer
        v-model="drawerVisible"
        title="提交处理结果"
        size="500px"
        :before-close="handleDrawerClose"
    >
      <el-form
          ref="resultFormRef"
          :model="resultForm"
          :rules="resultRules"
          label-position="top"
      >
        <el-form-item label="工单信息">
          <el-descriptions :column="1" border size="small">
            <el-descriptions-item label="工单编号">
              {{ currentWorkOrder?.work_order_no }}
            </el-descriptions-item>
            <el-descriptions-item label="报修人">
              {{ currentWorkOrder?.name }}
            </el-descriptions-item>
            <el-descriptions-item label="故障地点">
              {{ currentWorkOrder?.location }}
            </el-descriptions-item>
            <el-descriptions-item label="故障描述">
              {{ currentWorkOrder?.description }}
            </el-descriptions-item>
          </el-descriptions>
        </el-form-item>

        <el-form-item label="处理类型" prop="handle_type">
          <el-select v-model="resultForm.handle_type" placeholder="请选择处理类型" style="width: 100%">
            <el-option label="诊断" value="diagnose" />
            <el-option label="维修" value="repair" />
            <el-option label="配置" value="configure" />
            <el-option label="其他" value="other" />
          </el-select>
        </el-form-item>

        <el-form-item label="处理内容" prop="content">
          <el-input
              v-model="resultForm.content"
              type="textarea"
              :rows="4"
              placeholder="详细记录处理过程"
              maxlength="1000"
              show-word-limit
          />
        </el-form-item>

        <el-form-item label="处理结果" prop="result">
          <el-input
              v-model="resultForm.result"
              type="textarea"
              :rows="3"
              placeholder="填写最终处理结果"
              maxlength="500"
              show-word-limit
          />
        </el-form-item>
      </el-form>

      <template #footer>
        <div style="display: flex; justify-content: flex-end; gap: 10px">
          <el-button @click="handleDrawerClose">取消</el-button>
          <el-button type="primary" @click="handleSubmitResultConfirm" :loading="submitLoading">
            提交
          </el-button>
        </div>
      </template>
    </el-drawer>
  </div>
</template>

<style scoped>
.engineer-workorder-container {
  padding: 15px;
  background-color: #f5f7fa;
  min-height: 100vh;
}

.search-card {
  margin-bottom: 15px;
}

.search-form {
  display: flex;
  flex-wrap: wrap;
}

.table-card {
  min-height: 60vh;

}

.user-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.user-name {
  font-weight: 600;
  color: #333;
}

.user-phone {
  font-size: 12px;
  color: #666;
}

.action-buttons {
  display: flex;
  gap: 5px;
}

:deep(.el-drawer__header) {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e6e6e6;
}

:deep(.el-drawer__body) {
  padding: 20px;
}

:deep(.el-descriptions__label) {
  width: 100px;
}
</style>
