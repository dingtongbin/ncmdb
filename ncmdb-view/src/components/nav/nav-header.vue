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
import {useRoute, useRouter} from "vue-router";
import { ref, onMounted } from 'vue'
import axios from "axios";
import {API_URL, request} from "../../api/request.js";
import { ElMessage, ElMessageBox } from 'element-plus';
import NavLogo from "./nav-logo.vue";
import ShowNavSideButton from "./show-nav-side-button.vue";
import router from "../../router.js";
import {storeSetting} from "../../pinia/store_setting.js";
import {ArrowDown, ArrowUp, User} from "@element-plus/icons-vue";

const store_setting=storeSetting()
const route = useRoute()

// 用户信息
const userInfo = ref({
  user_id: '',
  username: '',
  real_name: '',
  department: '',
  phone: ''
})

// 修改密码相关
const showPasswordDialog = ref(false)
const passwordForm = ref({
  old_password: '',
  new_password1: '',
  new_password2: ''
})
const passwordLoading = ref(false)

// 加载用户信息
const loadUserInfo = async () => {
  try {
    const res = await request.get(API_URL+'/api/user_info/')
    if (res.data.status === 'success') {
      userInfo.value = res.data.data
    }
  } catch (error) {
    console.error('加载用户信息失败:', error)
  }
}

// 显示修改密码弹窗
const showChangePassword = () => {
  passwordForm.value = {
    old_password: '',
    new_password1: '',
    new_password2: ''
  }
  showPasswordDialog.value = true
}

// 前端验证密码
const validatePassword = (password) => {
  if (password.length < 8) {
    ElMessage.warning('密码长度至少为 8 位')
    return false
  }
  if (!/[a-z]/.test(password)) {
    ElMessage.warning('密码必须包含小写字母')
    return false
  }
  if (!/[A-Z]/.test(password)) {
    ElMessage.warning('密码必须包含大写字母')
    return false
  }
  if (!/[0-9]/.test(password)) {
    ElMessage.warning('密码必须包含数字')
    return false
  }
  return true
}

// 提交修改密码
const submitChangePassword = async () => {
  // 验证必填项
  if (!passwordForm.value.old_password || !passwordForm.value.new_password1 || !passwordForm.value.new_password2) {
    ElMessage.warning('请填写完整信息')
    return
  }

  // 验证两次密码是否一致
  if (passwordForm.value.new_password1 !== passwordForm.value.new_password2) {
    ElMessage.error('两次输入的新密码不一致')
    return
  }

  // 验证新密码复杂度
  if (!validatePassword(passwordForm.value.new_password1)) {
    return
  }

  passwordLoading.value = true

  try {
    const res = await request.post(API_URL+'/api/change_password/', {
      old_password: passwordForm.value.old_password,
      new_password1: passwordForm.value.new_password1,
      new_password2: passwordForm.value.new_password2
    })

    if (res.data.status === 'success') {
      ElMessageBox.alert('密码修改成功，请重新登录', '提示', {
        confirmButtonText: '确定',
        type: 'success',
        callback: () => {
          // 清除存储的 token
          document.cookie = null;
          localStorage.removeItem('csrftoken');
          sessionStorage.removeItem('csrftoken');
          localStorage.removeItem('user_info');
          // 跳转到登录页
          showPasswordDialog.value=false
          router.push('/login');
        }
      })
    } else {
      ElMessage.error(res.data.message || '修改密码失败')
    }
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error(error.response?.data?.message || '修改密码失败')
  } finally {
    passwordLoading.value = false
  }
}

// 添加退出登录函数
const logout = () => {
  // 清除 csrftoken
  document.cookie = null;
  localStorage.removeItem('csrftoken');
  sessionStorage.removeItem('csrftoken');
  localStorage.removeItem('user_info');
  // 跳转到登录页
  router.push('/login');
}
const showAIGC=ref(false)

// 监听路由变化，更新菜单激活状态

// 组件挂载时加载用户信息
onMounted(() => {
  loadUserInfo()
})

</script>

<template>
  <el-affix  v-if="!store_setting.isLoginRoute" :offset="0">
    <div style="background-color: #409EFF;height: 60px;display: flex;justify-content: space-between;padding: 0 1% 0 1%">
      <!--  logo-->
      <div style="display:flex;align-items: center;justify-content: center;width: 200px;color: white;
            font-weight: bold;
            ">

        <nav-logo></nav-logo>

        <span style="margin-left: 2%;font-size: 0.9rem">网络运维资产管理系统</span>
        <show-nav-side-button></show-nav-side-button>
      </div>
      <div style="display: flex;justify-content: center;align-items: center">

        <!--<span>-->
        <!--  <el-button @click="showAIGC=true" type="default" color="#000000"  text>AI 助手</el-button>-->
        <!--</span>-->
        <div style="margin-right: 1%;">


          <el-dropdown
              trigger="click"
              style="height: 60px"
          >
            <div style="display: flex; align-items: center; cursor: pointer;">

        <div style="color: white; margin-left: 8px;
         white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
          max-width: 150px;
          display: flex;
          align-items: end;
          height: 1rem;


        ">

         <span style="height: 1rem;">
          {{ userInfo.username }}({{userInfo.real_name}})
          </span>
          <el-icon>
            <arrow-down  />

          </el-icon>
        </div>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="showChangePassword">修改密码</el-dropdown-item>
                <el-dropdown-item @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>

        </div>

      </div>
    </div>
  </el-affix>

  <!-- 修改密码弹窗 -->
  <el-dialog
      v-model="showPasswordDialog"
      title="修改密码"
      width="500px"
      :close-on-click-modal="false"
  >
    <el-form :model="passwordForm" label-width="100px">
      <el-form-item label="旧密码" required>
        <el-input
            v-model="passwordForm.old_password"
            type="password"
            placeholder="请输入旧密码"
            show-password
        />
      </el-form-item>
      <el-form-item label="新密码" required>
        <el-input
            v-model="passwordForm.new_password1"
            type="password"
            placeholder="请输入新密码（至少 8 位，包含大小写字母和数字）"
            show-password
        />
      </el-form-item>
      <el-form-item label="确认新密码" required>
        <el-input
            v-model="passwordForm.new_password2"
            type="password"
            placeholder="请再次输入新密码"
            show-password
        />
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="showPasswordDialog = false">取消</el-button>
      <el-button type="primary" @click="submitChangePassword" :loading="passwordLoading">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<style scoped>

</style>
