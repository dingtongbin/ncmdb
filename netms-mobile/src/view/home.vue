<script setup>
// 导入依赖
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { getRepairRequests, submitRepairRequest } from '../api/api.js'
import { formatTimeAgo } from '../utils/timeFormat.js'
import { useRouter } from 'vue-router'

// 当前激活的标签页：'list'-工单列表，'submit'-创建工单
const activeTab = ref('list')

// 工单列表数据
const repairList = ref([])

const router = useRouter()

// 加载状态标识
const loading = ref(false)

// 表单数据对象
const form = ref({
  location: '',           // 故障地点
  description: '',        // 故障描述
  level: 'normal'         // 紧急程度：low/normal/high/urgent
})
// 页面加载时获取列表
onMounted(() => {
  loadRepairs()
})

// 跳转到工单详情页
const goToDetail = (id) => {
  router.push(`/workorder/${id}`)
}
// 提交按钮的加载状态
const submitLoading = ref(false)

// 加载工单列表
const loadRepairs = async () => {
  loading.value = true
  try {
    const data = await getRepairRequests()
    repairList.value = data
    ElMessage.success('加载成功')
  } catch (error) {
    console.error('加载失败:', error)
    ElMessage.error('加载工单列表失败')
  } finally {
    loading.value = false
  }
}

// 提交工单
const handleSubmit = async () => {
  // 表单验证：检查地点和描述是否填写
  if (!form.value.location || !form.value.description) {
    ElMessage.warning('请填写完整信息')
    return
  }

  submitLoading.value = true
  try {
    // 准备提交数据
    const submitData = {
      location: form.value.location,      // 故障地点
      level: form.value.level,            // 紧急程度
      description: form.value.description // 故障描述
    }

    // 调用 API 提交工单
    const result = await submitRepairRequest(submitData)

    // 处理提交结果
    if (result.success) {
      ElMessage.success(`工单提交成功！工单编号：${result.data.work_order_no}`)
      // 重置表单
      form.value = {
        location: '',
        description: '',
        level: 'normal'
      }
      // 切换到列表标签
      activeTab.value = 'list'
      // 刷新列表
      loadRepairs()
    } else {
      ElMessage.error(result.error || '提交失败')
    }
  } catch (error) {
    console.error('提交失败:', error)
    ElMessage.error('提交失败，请重试')
  } finally {
    submitLoading.value = false
  }
}

// 格式化时间：将时间字符串转换为"x 分钟前/小时前/天前"
const formatTime = (timeStr) => {
  return formatTimeAgo(timeStr)
}

// 获取状态文本：显示工单当前状态
const getStatusText = (item) => {
  return item.status_display || '未知状态'
}

// 获取状态类型：用于标签颜色
const getStatusType = (item) => {
  const statusMap = {
    'pending': 'info',      // 待受理 - 灰色
    'accepted': 'warning',  // 已受理 - 橙色
    'processing': 'primary',// 处理中 - 蓝色
    'resolved': 'success',  // 已解决 - 绿色
    'completed': 'success'  // 已完成 - 绿色
  }
  return statusMap[item.status] || 'info'
}

// 获取紧急程度文本：将英文转换为中文显示
const getLevelText = (item) => {
  const levelMap = {
    'low': '低',
    'normal': '一般',
    'high': '高',
    'urgent': '紧急'
  }
  return levelMap[item.level] || '一般'
}

// 获取紧急程度标签类型：用于标签颜色
const getLevelType = (level) => {
  const typeMap = {
    'low': 'info',
    'normal': '',
    'high': 'warning',
    'urgent': 'danger'
  }
  return typeMap[level] || ''
}

// 页面加载时获取列表
onMounted(() => {
  loadRepairs()
})
</script>

<template>
  <div class="home-container">
    <!-- 标签页容器 -->
    <el-tabs v-model="activeTab" class="content-tabs">
      <!-- 工单列表标签页 -->
      <el-tab-pane label="我的工单" name="list">
        <div class="tab-content">
          <el-scrollbar height="calc(100vh - 180px)">
            <div v-loading="loading" class="repair-list">
              <!-- 工单卡片 -->
              <div
                  v-for="item in repairList"
                  :key="item.id"
                  class="repair-card"
                  @click="goToDetail(item.id)"
              >
                <div class="card-left">
                  <!-- 卡片头部：工单号 -->
                  <div class="card-header">
                    <span class="work-order-no">工单 {{ item.work_order_no }}</span>
                  </div>
                  <!-- 工单描述 -->
                  <div class="card-title">{{ item.description }}</div>
                  <!-- 卡片信息：地点和时间 -->
                  <div class="card-info">
                    <span class="location">{{ item.location }}</span>
                    <span class="time">{{ formatTime(item.created_at) }}</span>
                  </div>
                </div>
                <div class="card-right">
                  <!-- 标签组：紧急程度和状态垂直排列 -->
                  <div class="tag-group">
                    <el-tag :type="getLevelType(item.level)" size="small">
                      {{ getLevelText(item) }}
                    </el-tag>
                    <el-tag :type="getStatusType(item)" size="small">
                      {{ getStatusText(item) }}
                    </el-tag>
                  </div>
                </div>
              </div>

              <!-- 空状态提示 -->
              <el-empty v-if="!loading && repairList.length === 0" description="暂无工单" />
            </div>
          </el-scrollbar>
        </div>
      </el-tab-pane>

      <!-- 创建工单标签页 -->
      <el-tab-pane label="创建工单" name="submit">
        <div class="tab-content">
          <el-scrollbar height="calc(100vh - 180px)">
            <div class="form-container">
              <el-form :model="form" label-position="top">
                <!-- 故障地点输入 -->
                <el-form-item label="故障地点">
                  <el-input
                      v-model="form.location"
                      placeholder="请输入故障地点"
                      clearable
                      prefix-icon="Location"
                  />
                </el-form-item>

                <!-- 紧急程度选择 -->
                <el-form-item label="紧急程度">
                  <el-select v-model="form.level" style="width: 100%" placeholder="请选择紧急程度">
                    <el-option label="低" value="low" />
                    <el-option label="一般" value="normal" />
                    <el-option label="高" value="high" />
                    <el-option label="紧急" value="urgent" />
                  </el-select>
                </el-form-item>

                <!-- 故障描述输入 -->
                <el-form-item label="故障描述">
                  <el-input
                      v-model="form.description"
                      type="textarea"
                      :rows="6"
                      placeholder="请详细描述故障情况，例如：网络无法连接、打印机故障等"
                      maxlength="1000"
                      show-word-limit
                  />
                </el-form-item>

                <!-- 提交按钮 -->
                <el-form-item>
                  <el-button
                      type="primary"
                      size="large"
                      style="width: 100%"
                      :loading="submitLoading"
                      @click="handleSubmit"
                  >
                    {{ submitLoading ? '提交中...' : '提交工单' }}
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-scrollbar>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<style scoped>
/* 主容器样式 */
.home-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background-color: #f5f7fa;
  padding: 10px;
  box-sizing: border-box;
}

/* 标签页容器样式 */
.content-tabs {
  flex: 1;
  background: #f5f7fa;
  overflow: hidden;
  max-width: 900px;
  margin: 0 auto;
  width: 100%;
}

/* 标签页头部样式 */
:deep(.el-tabs__header) {
  margin-bottom: 10px;
  background: white;
  padding: 10px 15px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 标签页内容区样式 */
:deep(.el-tabs__content) {
  padding: 0;
}

/* 标签内容卡片样式 */
.tab-content {
  background: white;
  border-radius: 8px;
  padding: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

/* 工单列表容器样式 */
.repair-list {
  min-height: 200px;
}

/* 工单卡片样式 */
.repair-card {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  margin-bottom: 12px;
  transition: all 0.3s;
  background: #fafafa;
}

/* 工单卡片悬停效果 */
.repair-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
  background: white;
}

/* 卡片左侧区域 */
.card-left {
  flex: 1;
  overflow: hidden;
}

/* 卡片头部区域 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

/* 工单编号样式 */
.work-order-no {
  font-size: 13px;
  color: #666;
  font-weight: 600;
}

/* 卡片标题样式 */
.card-title {
  font-size: 15px;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 卡片信息区域 */
.card-info {
  display: flex;
  gap: 15px;
  font-size: 13px;
  color: #666;
}

/* 地点和时间样式 */
.location, .time {
  display: flex;
  align-items: center;
  gap: 4px;
}

/* 卡片右侧区域 */
.card-right {
  margin-left: 15px;
  flex-shrink: 0;
}

/* 表单容器样式 */
.form-container {
  max-width: 600px;
  margin: 0 auto;
}

/* 表单项间距 */
:deep(.el-form-item) {
  margin-bottom: 22px;
}

/* 表单标签样式 */
:deep(.el-form-item__label) {
  font-weight: 600;
  color: #333;
  font-size: 14px;
}

/* 文本域样式 */
:deep(.el-textarea__inner) {
  font-size: 14px;
}

/* 媒体查询 - 小屏幕适配 */
@media (max-width: 768px) {
  /* 容器间距调整 */
  .home-container {
    padding: 5px;
  }

  /* 卡片改为纵向布局 */
  .repair-card {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
    padding: 12px;
  }

  /* 右侧区域占满一行 */
  .card-right {
    margin-left: 0;
    width: 100%;
    display: flex;
    justify-content: flex-end;
  }

  /* 标题字体调小 */
  .card-title {
    font-size: 14px;
  }

  /* 信息纵向排列 */
  .card-info {
    flex-direction: column;
    gap: 6px;
    font-size: 12px;
  }

  /* 内容区域内边距调整 */
  .tab-content {
    padding: 10px;
  }
}
</style>
