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
import {computed, ref, watch} from 'vue'
import { useRoute } from 'vue-router'
import {storeSetting} from "../../pinia/store_setting.js";
const store_setting=storeSetting()
const route = useRoute()
// 监听路由变化，更新菜单激活状态
// 计算菜单激活项
const menus = computed(() => {
  if (route.path.startsWith('/device/network/detail/')) {
    return '/device/network'
  }
  return route.path
})

// 监听路由变化，更新菜单激活状态
watch(
    () => route.path,
    (newPath) => {
      store_setting.isLoginRoute = newPath === '/login'
    },
    { immediate: true }
)
</script>
<template>
  <el-scrollbar v-if="store_setting.show_side && !store_setting.isLoginRoute" style="height: 90vh;width: 200px;background-color: #ffffff;" >
    <el-menu

        v-model:default-active="menus"
        style="width: 200px;border: none;"
        class="el-menu-vertical-demo"
        router
        background-color="rgba(211, 211, 211, 0)"
        active-text-color="#409EFF"
        text-color="#000000"
    >
      <el-menu-item index="/">仪表盘</el-menu-item>
      <el-sub-menu index="1">
        <template #title>
          <span>网络管理</span>
        </template>
        <el-menu-item index="/network_device">网络设备</el-menu-item>
        <el-menu-item index="/terminal">终端管理</el-menu-item>
        <el-menu-item index="/ipam">IP子网管理</el-menu-item>
      </el-sub-menu>
      <el-sub-menu index="2">
        <template #title>

          <span>监控告警信息</span>
        </template>
        <el-menu-item index="/alert/alert">告警信息</el-menu-item>
        <el-menu-item index="/alert/webhook">WebHook API管理</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/Infrastructure">基础设施管理</el-menu-item>
      <el-sub-menu index="4">
        <template #title>
          <span>运维管理</span>
        </template>
        <el-menu-item index="/patrol_plan">巡检计划</el-menu-item>
        <el-menu-item index="/patrol_task">计划任务</el-menu-item>
      </el-sub-menu>
      <el-menu-item index="/inventory">库存管理</el-menu-item>
      <el-menu-item index="/contact">联系人</el-menu-item>
      <el-menu-item index="/filem">运维文件管理</el-menu-item>
      <el-menu-item index="/repair">故障报修信息</el-menu-item>
    </el-menu>
  </el-scrollbar>

</template>
<style scoped>
/* 覆盖 el-menu-item 选中时的背景色 */
.el-menu .el-menu-item.is-active {
  background-color: rgba(64, 158, 255, 0.1) !important; /* 你想要的颜色 */
  color: #409EFF !important;
  font-weight: bold;
}



</style>