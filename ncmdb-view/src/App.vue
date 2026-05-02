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

import NavHeader from "./components/nav/nav-header.vue";
import NavSide from "./components/nav/nav-side.vue";
import {storeSetting} from "./pinia/store_setting.js";
const store_setting=storeSetting()
</script>

<template>

      <el-container>
        <el-header style="padding: 0"><nav-header /></el-header>
        <el-container style="padding: 0">
          <el-aside v-if="store_setting.show_side" width="201px" style="border-right: rgba(48,49,51,0.3) 1px solid;box-sizing: border-box"><nav-side/></el-aside>
          <el-main style="height: calc(100vh-60px)">
            <router-view></router-view>
          </el-main>
        </el-container>
      </el-container>

  </template>
<style scoped>

</style>
