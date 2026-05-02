<script setup>
import { computed, ref ,onMounted} from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {changePassword, getUserInfo} from './api/api.js'

const route = useRoute()
const router = useRouter()
const userInfo = ref(null)
// 判断是否显示页头（登录页和 404 页不显示）
const showHeader = computed(() => {
  return route.path !== '/login'
})

// 修改密码弹窗相关
const passwordDialogVisible = ref(false)
const passwordForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})
const passwordLoading = ref(false)

// 打开修改密码弹窗
const openPasswordDialog = () => {
  passwordForm.value = {
    old_password: '',
    new_password1: '',
    new_password2: ''
  }
  passwordDialogVisible.value = true
}

// 提交修改密码
const handleSubmitPassword = async () => {
  const { old_password, new_password1, new_password2 } = passwordForm.value

  // 前端验证必填项
  if (!old_password || !new_password1 || !new_password2) {
    ElMessage.warning('请填写所有字段')
    return
  }

  // 前端验证密码长度
  if (new_password1.length < 8) {
    ElMessage.warning('密码长度至少为 8 位')
    return
  }

  // 前端验证密码复杂度
  if (!/[a-z]/.test(new_password1)) {
    ElMessage.warning('密码必须包含小写字母')
    return
  }

  if (!/[A-Z]/.test(new_password1)) {
    ElMessage.warning('密码必须包含大写字母')
    return
  }

  if (!/[0-9]/.test(new_password1)) {
    ElMessage.warning('密码必须包含数字')
    return
  }

  // 前端验证两次密码是否一致
  if (new_password1 !== new_password2) {
    ElMessage.error('两次输入的新密码不一致')
    return
  }

  passwordLoading.value = true

  try {
    const res = await changePassword({
      old_password: old_password,
      new_password1: new_password1,
      new_password2: new_password2
    })

    if (res.status === 'success') {
      ElMessage.success(res.message || '密码修改成功，请重新登录')
      passwordDialogVisible.value = false

      // 清除 token
      localStorage.removeItem('access_token')
      localStorage.removeItem('user_info')
      document.cookie = null
      sessionStorage.removeItem('csrftoken')
      localStorage.removeItem('csrftoken')

      // 跳转到登录页
      setTimeout(() => {
        router.push('/login')
      }, 500)
    } else {
      ElMessage.error(res.message || '密码修改失败')
    }
  } catch (error) {
    const errorMsg = error.response?.data?.message || error.message || '密码修改失败'
    ElMessage.error(errorMsg)
  } finally {
    passwordLoading.value = false
  }
}

// 退出登录
const handleLogout = () => {
  localStorage.removeItem('access_token')
  router.replace('/login')
  ElMessage.success('已退出登录')
}
// 获取用户信息
const fetchUserInfo = async () => {
  try {
    const res = await getUserInfo()
    console.log('用户信息:', res)
    userInfo.value = res.data

  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}
onMounted(() => {
  fetchUserInfo()
})
</script>

<template>
  <div class="app-container">
    <!-- 页头 -->
    <el-header v-if="showHeader" class="app-header">
      <div class="header-content">
        <h1 class="header-title">网络系统工单</h1>
        <div class="header-right">
          <span class="welcome-text">{{ userInfo?.username || '欢迎使用' }}({{userInfo?.real_name}})</span>
          <el-dropdown trigger="click">
            <el-button style="color: white" type="primary" plain text   size="large">
              设置
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="openPasswordDialog">修改密码</el-dropdown-item>
                <el-dropdown-item divided @click="handleLogout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </el-header>

    <!-- 主内容区 -->
    <div class="main-wrapper">
      <router-view></router-view>
    </div>

    <!-- 修改密码弹窗 -->
    <el-dialog
        v-model="passwordDialogVisible"
        title="修改密码"
        width="90%"
        max-width="400px"
        :close-on-click-modal="false"
    >
      <el-form :model="passwordForm" label-position="top">
        <el-form-item label="旧密码">
          <el-input
              v-model="passwordForm.old_password"
              type="password"
              placeholder="请输入旧密码"
              show-password
          />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input
              v-model="passwordForm.new_password1"
              type="password"
              placeholder="请输入新密码（至少 8 位，包含大小写字母和数字）"
              show-password
          />
        </el-form-item>
        <el-form-item label="确认新密码">
          <el-input
              v-model="passwordForm.new_password2"
              type="password"
              placeholder="请再次输入新密码"
              show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <div style="display: flex; justify-content: flex-end; gap: 10px;">
          <el-button @click="passwordDialogVisible = false">取消</el-button>
          <el-button type="primary" :loading="passwordLoading" @click="handleSubmitPassword">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.app-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.app-header {
  width: 100%;
  background: linear-gradient(135deg, #409EFF 0%, #706f6f 100%);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 100;
}

.header-content {
  max-width: 1200px;
  height: 100%;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-title {
  margin: 0;
  color: white;
  font-size: 22px;
  font-weight: 600;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 15px;
}

.welcome-text {
  color: white;
  font-size: 14px;
}

.main-wrapper {
  flex: 1;
  overflow: hidden;
  width: 100%;
  display: flex;
}

/* 媒体查询 - 小屏幕适配 */
@media (max-width: 768px) {
  .header-title {
    font-size: 18px;
  }

  .welcome-text {
    font-size: 12px;
  }

  .header-content {
    padding: 0 15px;
  }
}
</style>
