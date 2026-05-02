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

import {ref,watch} from "vue";
import {useRoute, useRouter} from "vue-router";
import { ElMessage } from 'element-plus'

import {ArrowLeftBold, Tools} from '@element-plus/icons-vue'
import { changePassword } from '../api/api.js'

const route = useRoute()
const router = useRouter()
const is_login = ref(false)
const tab_text_value=ref("XX 公司网络维护")
const back_show = ref(false)
const setting_show = ref(true)
const logo=ref(true)
const tab_text = ref([
  {path: '/', text: 'XX 公司网络维护',logo: true},
  {path: '/repair_record', text: '报修记录',logo: false},
  {path: '/self_service', text: '自助服务',logo: false},
])

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

// 添加退出登录函数
const logout = () => {
  // 清除 Cookie 中的 csrftoken
  document.cookie = null;

  // 如果 csrftoken 存储在 localStorage 中，也需要清除
  localStorage.removeItem('csrftoken');

  // 如果 csrftoken 存储在 sessionStorage 中，也需要清除
  sessionStorage.removeItem('csrftoken');

  localStorage.removeItem('user_info');
  // 跳转到登录页
  router.push('login');
}

// 监听路由变化
watch(
    () => route.path,
    (newPath) => {
      logo.value=tab_text.value.find(item => item.path === newPath)?.logo
      tab_text_value.value = tab_text.value.find(item => item.path === newPath)?.text
      is_login.value = newPath === '/login'

      // 如果不是首页，则显示返回按钮，隐藏设置按钮
      if (newPath !== '/') {
        back_show.value = true
        setting_show.value = false
      } else {
        back_show.value = false
        setting_show.value = true
      }

    },
    { immediate: true } // 立即执行一次
)
</script>

<template>
  <el-affix :offset="0"   v-if="!is_login">
    <div
        style="background-color: #409EFF;height: 50px;display: flex;justify-content: space-between;align-items: center"
    >
      <div v-if="back_show">
        <el-icon color="#FFFFFF" size="25"
                 style="margin-left: 1%"
                 @click="router.back()"
        >
          <ArrowLeftBold/>
        </el-icon>
      </div>
      <div v-else></div>
      <!--  logo-->
      <div v-if="logo" style="display:flex;align-items: center;justify-content: center;width: 200px;color: white;
            font-weight: bold;
            ">
        <el-icon size="35" >
          <svg class="icon" height="200" p-id="4552" t="1758175232404" version="1.1"
               viewBox="0 0 1024 1024" width="200" xmlns="http://www.w3.org/2000/svg">
            <path
                d="M512 55.466667c-38.4 0-76.8 4.266667-110.933333 12.8C204.8 119.466667 55.466667 298.666667 55.466667 512S260.266667 968.533333 512 968.533333s76.8-4.266667 110.933333-12.8c200.533333-51.2 345.6-230.4 345.6-443.733333S763.733333 55.466667 512 55.466667z m285.866667 183.466666c-34.133333 8.533333-72.533333 12.8-115.2 21.333334-8.533333-42.666667-21.333333-81.066667-34.133334-119.466667 55.466667 21.333333 106.666667 55.466667 149.333334 98.133333z m-358.4-115.2c46.933333-8.533333 93.866667-8.533333 140.8 0 17.066667 42.666667 34.133333 89.6 46.933333 145.066667-38.4 0-81.066667 4.266667-132.266667 4.266667H388.266667c12.8-55.466667 29.866667-106.666667 51.2-145.066667z m-76.8 21.333334c-12.8 34.133333-25.6 72.533333-34.133334 115.2-42.666667-4.266667-76.8-12.8-106.666666-21.333334 38.4-42.666667 85.333333-76.8 140.8-98.133333z m-136.533334 640c34.133333-8.533333 72.533333-12.8 115.2-21.333334 8.533333 42.666667 21.333333 81.066667 34.133334 119.466667-55.466667-21.333333-106.666667-55.466667-149.333334-98.133333z m358.4 115.2c-46.933333 8.533333-93.866667 8.533333-140.8 0-17.066667-42.666667-34.133333-89.6-46.933333-145.066667 38.4 0 81.066667-4.266667 132.266667-4.266667h106.666666c-12.8 55.466667-29.866667 106.666667-51.2 145.066667z m76.8-21.333334c12.8-34.133333 25.6-72.533333 34.133334-115.2 42.666667 4.266667 76.8 12.8 106.666666 21.333334-38.4 42.666667-85.333333 76.8-140.8 98.133333z m179.2-145.066666c-42.666667-12.8-102.4-25.6-170.666666-29.866667-42.666667 0-89.6-4.266667-140.8-4.266667s-119.466667 0-170.666667 8.533334v0c-72.533333 8.533333-123.733333 17.066667-174.933333 29.866666-42.666667-64-68.266667-140.8-68.266667-221.866666s25.6-157.866667 68.266667-221.866667c42.666667 17.066667 102.4 25.6 170.666666 29.866667 42.666667 0 89.6 4.266667 140.8 4.266666s119.466667 0 170.666667-8.533333c72.533333-8.533333 123.733333-17.066667 174.933333-29.866667 42.666667 64 68.266667 140.8 68.266667 221.866667s-25.6 157.866667-68.266667 221.866667z"
                fill="#ffffff" p-id="4553"></path>
            <path
                d="M256 396.8c-17.066667 0-29.866667 12.8-29.866667 29.866667v170.666666c0 17.066667 12.8 29.866667 29.866667 29.866667s29.866667-12.8 29.866667-29.866667v-170.666666c0-17.066667-12.8-29.866667-29.866667-29.866667zM439.466667 396.8H341.333333c-17.066667 0-29.866667 12.8-29.866666 29.866667v170.666666c0 17.066667 12.8 29.866667 29.866666 29.866667s29.866667-12.8 29.866667-29.866667v-46.933333h68.266667c17.066667 0 29.866667-12.8 29.866666-29.866667V426.666667c0-17.066667-12.8-29.866667-29.866666-29.866667z m-29.866667 93.866667h-38.4v-34.133334h38.4v34.133334zM627.2 396.8c-17.066667 0-34.133333 4.266667-34.133333 21.333333l-25.6 98.133334-25.6-98.133334c0-17.066667-21.333333-25.6-34.133334-21.333333-17.066667 0-25.6 21.333333-21.333333 34.133333l42.666667 170.666667c0 12.8 17.066667 21.333333 29.866666 21.333333h21.333334c12.8 0 25.6-8.533333 29.866666-21.333333l42.666667-170.666667c0-17.066667-4.266667-34.133333-21.333333-34.133333zM802.133333 499.2h-4.266666V426.666667c0-17.066667-12.8-29.866667-29.866667-29.866667s-29.866667 12.8-29.866667 29.866667v72.533333h-25.6V426.666667c0-17.066667-12.8-29.866667-29.866666-29.866667s-29.866667 12.8-29.866667 29.866667v102.4c0 17.066667 12.8 29.866667 29.866667 29.866666h55.466666v38.4c0 17.066667 12.8 29.866667 29.866667 29.866667s29.866667-12.8 29.866667-29.866667v-38.4h4.266666c17.066667 0 29.866667-12.8 29.866667-29.866666s-12.8-29.866667-29.866667-29.866667z"
                fill="#ffffff" p-id="4554"></path>
          </svg>
        </el-icon>
        <span style="margin-left: 5%;font-size: 1.2rem">{{ tab_text_value }}</span>
      </div>
      <div v-else style="display:flex;align-items: center;justify-content: center;width: 200px;color: white;
            font-weight: bold;
            ">
        <span style="font-size: 1.2rem">{{ tab_text_value }}</span>
      </div>

      <div v-if="setting_show" style="display: flex;justify-content: center;align-items: center">
        <div style="margin-right: 100%;">
          <el-dropdown trigger="click">
            <el-icon color="#FFFFFF" size="25">
              <Tools/>
            </el-icon>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="logout">个人信息</el-dropdown-item>
                <el-dropdown-item @click="openPasswordDialog">修改密码</el-dropdown-item>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
      <div v-else></div>
    </div>
  </el-affix>

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
</template>

<style scoped>

</style>
