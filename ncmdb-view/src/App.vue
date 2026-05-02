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
