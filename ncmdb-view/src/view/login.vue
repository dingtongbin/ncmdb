<!-- src/view/login.vue -->
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {login} from "../api/login.js";
import {storeSetting} from "../pinia/store_setting.js";

const router = useRouter()
const loading= ref(false)
const loginForm = ref({
  username: '',
  password: ''
})
const store_setting=storeSetting()
const handleLogin = async () => {

  if (!loginForm.value.username || !loginForm.value.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  loading.value = true
  try {

    const res = await login(loginForm.value.username, loginForm.value.password)
    store_setting.access_token=res.access
    localStorage.setItem('access_token',res.access)
    // 跳转到首页
    ElMessage.success('登录成功')
    await router.replace('/')
  } catch (error) {
    ElMessage.error(error.message || '登录失败')
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-overlay">
    <div class="login-wrapper">
      <div class="login-split-container">
        <!-- 左侧：公司图片展示 -->
        <div class="left-panel">
          <div class="company-info">
            <div class="company-logo">
              <svg t="1758175232404" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" width="200" height="200"><path d="M512 55.466667c-38.4 0-76.8 4.266667-110.933333 12.8C204.8 119.466667 55.466667 298.666667 55.466667 512S260.266667 968.533333 512 968.533333s76.8-4.266667 110.933333-12.8c200.533333-51.2 345.6-230.4 345.6-443.733333S763.733333 55.466667 512 55.466667z m285.866667 183.466666c-34.133333 8.533333-72.533333 12.8-115.2 21.333334-8.533333-42.666667-21.333333-81.066667-34.133334-119.466667 55.466667 21.333333 106.666667 55.466667 149.333334 98.133333z m-358.4-115.2c46.933333-8.533333 93.866667-8.533333 140.8 0 17.066667 42.666667 34.133333 89.6 46.933333 145.066667-38.4 0-81.066667 4.266667-132.266667 4.266667H388.266667c12.8-55.466667 29.866667-106.666667 51.2-145.066667z m-76.8 21.333334c-12.8 34.133333-25.6 72.533333-34.133334 115.2-42.666667-4.266667-76.8-12.8-106.666666-21.333334 38.4-42.666667 85.333333-76.8 140.8-98.133333z m-136.533334 640c34.133333-8.533333 72.533333-12.8 115.2-21.333334 8.533333 42.666667 21.333333 81.066667 34.133334 119.466667-55.466667-21.333333-106.666667-55.466667-149.333334-98.133333z m358.4 115.2c-46.933333 8.533333-93.866667 8.533333-140.8 0-17.066667-42.666667-34.133333-89.6-46.933333-145.066667 38.4 0 81.066667-4.266667 132.266667-4.266667h106.666666c-12.8 55.466667-29.866667 106.666667-51.2 145.066667z m76.8-21.333334c12.8-34.133333 25.6-72.533333 34.133334-115.2 42.666667 4.266667 76.8 12.8 106.666666 21.333334-38.4 42.666667-85.333333 76.8-140.8 98.133333z m179.2-145.066666c-42.666667-12.8-102.4-25.6-170.666666-29.866667-42.666667 0-89.6-4.266667-140.8-4.266667s-119.466667 0-170.666667 8.533334v0c-72.533333 8.533333-123.733333 17.066667-174.933333 29.866666-42.666667-64-68.266667-140.8-68.266667-221.866666s25.6-157.866667 68.266667-221.866667c42.666667 17.066667 102.4 25.6 170.666666 29.866667 42.666667 0 89.6 4.266667 140.8 4.266666s119.466667 0 170.666667-8.533333c72.533333-8.533333 123.733333-17.066667 174.933333-29.866667 42.666667 64 68.266667 140.8 68.266667 221.866667s-25.6 157.866667-68.266667 221.866667z" fill="#ffffff"></path><path d="M256 396.8c-17.066667 0-29.866667 12.8-29.866667 29.866667v170.666666c0 17.066667 12.8 29.866667 29.866667 29.866667s29.866667-12.8 29.866667-29.866667v-170.666666c0-17.066667-12.8-29.866667-29.866667-29.866667zM439.466667 396.8H341.333333c-17.066667 0-29.866667 12.8-29.866666 29.866667v170.666666c0 17.066667 12.8 29.866667 29.866666 29.866667s29.866667-12.8 29.866667-29.866667v-46.933333h68.266667c17.066667 0 29.866667-12.8 29.866666-29.866667V426.666667c0-17.066667-12.8-29.866667-29.866666-29.866667z m-29.866667 93.866667h-38.4v-34.133334h38.4v34.133334zM627.2 396.8c-17.066667 0-34.133333 4.266667-34.133333 21.333333l-25.6 98.133334-25.6-98.133334c0-17.066667-21.333333-25.6-34.133334-21.333333-17.066667 0-25.6 21.333333-21.333333 34.133333l42.666667 170.666667c0 12.8 17.066667 21.333333 29.866666 21.333333h21.333334c12.8 0 25.6-8.533333 29.866666-21.333333l42.666667-170.666667c0-17.066667-4.266667-34.133333-21.333333-34.133333zM802.133333 499.2h-4.266666V426.666667c0-17.066667-12.8-29.866667-29.866667-29.866667s-29.866667 12.8-29.866667 29.866667v72.533333h-25.6V426.666667c0-17.066667-12.8-29.866667-29.866666-29.866667s-29.866667 12.8-29.866667 29.866667v102.4c0 17.066667 12.8 29.866667 29.866667 29.866666h55.466666v38.4c0 17.066667 12.8 29.866667 29.866667 29.866667s29.866667-12.8 29.866667-29.866667v-38.4h4.266666c17.066667 0 29.866667-12.8 29.866667-29.866666s-12.8-29.866667-29.866667-29.866667z" fill="#ffffff"></path></svg>
            </div>
            <div class="company-text-container">
              <h1 class="company-title">网络运维资产管理系统</h1>
              <span class="company-divider">|</span>
              <p class="company-subtitle">专业 · 高效 · 安全</p>
            </div>
          </div>
        </div>

        <!-- 右侧：登录表单 -->
        <div class="right-panel">
          <div class="login-box">
            <div class="login-header">
              <h2>系统登录</h2>
            </div>

            <el-form
                :model="loginForm"
                class="login-form"
                @keyup.enter="handleLogin"
            >
              <el-form-item>
                <el-input
                    v-model="loginForm.username"
                    placeholder="请输入用户名"
                    size="large"
                    clearable
                />
              </el-form-item>

              <el-form-item>
                <el-input
                    v-model="loginForm.password"
                    type="password"
                    placeholder="请输入密码"
                    size="large"
                    show-password
                />
              </el-form-item>

              <el-form-item>
                <el-button
                    type="primary"
                    size="large"
                    style="width: 100%"
                    :loading="loading"
                    @click="handleLogin"
                >
                  登录
                </el-button>
              </el-form-item>
            </el-form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #0a1628 0%, #1a3a6c 50%, #0d2137 100%);
  z-index: 9999;
  display: flex;
  justify-content: center;
  align-items: center;
  box-sizing: border-box;
}

.login-wrapper {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  box-sizing: border-box;
}

.login-split-container {
  display: flex;
  width: 100%;
  max-width: 900px;
  height: 500px;
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  box-sizing: border-box;
}


.left-panel {
  flex: 1;
  background: linear-gradient(135deg, #0f2c52 0%, #1a4d8c 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.left-panel::before {
  content: '';
  position: absolute;
  width: 100%;
  height: 100%;
  opacity: 0.4;
}

.company-info {
  text-align: center;
  color: white;
  z-index: 1;
  padding: 40px;
}

.company-logo {
  margin-bottom: 20px;
}

.company-text-container {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.company-title {
  font-size: 24px;
  font-weight: 700;
  margin: 0;
  white-space: nowrap;
}


.company-divider {
  color: rgba(255, 255, 255, 0.5);
  font-size: 18px;
}

.company-subtitle {
  font-size: 14px;
  opacity: 0.9;
  margin: 0;
  letter-spacing: 3px;
  white-space: nowrap;
}

.right-panel {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background: white;
  padding: 40px;
}

.login-box {
  width: 100%;
  max-width: 320px;
}

.login-header {
  text-align: center;
  margin-bottom: 40px;
}

.login-header h2 {
  color: #333;
  font-size: 28px;
  font-weight: 600;
  margin: 0;
}

.login-form {
  margin-top: 20px;
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
  padding: 12px 16px;
  transition: all 0.3s;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 0 0 2px rgba(26, 115, 238, 0.3);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(26, 115, 238, 0.6);
}


:deep(.el-button) {
  border-radius: 8px;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-split-container {
    flex-direction: column;
    height: auto;
    max-height: 100%;
  }

  .left-panel {
    padding: 30px 20px;
    min-height: 200px;
  }

  .company-text-container {
    flex-direction: column;
    gap: 10px;
  }

  .company-title {
    font-size: 20px;
  }

  .company-divider {
    display: none;
  }

  .company-subtitle {
    font-size: 12px;
  }

  .right-panel {
    padding: 30px 20px;
  }
}

@media (max-width: 480px) {
  .login-overlay {
    padding: 10px;
  }

  .login-split-container {
    border-radius: 12px;
  }

  .login-header h2 {
    font-size: 24px;
  }
}
</style>
