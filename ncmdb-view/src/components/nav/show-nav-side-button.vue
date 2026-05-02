<script setup>

import {Expand, Fold} from "@element-plus/icons-vue";
import {storeSetting} from "../../pinia/store_setting.js";
const store_setting=storeSetting()
</script>

<template>
  <button

@click="store_setting.show_side=!store_setting.show_side"
  >
    <el-icon size="20" v-if="store_setting.show_side"><Fold />

    </el-icon>
    <el-icon size="20" v-else>
     <Expand />
    </el-icon>
  </button>
</template>

<style scoped>
button{
  margin: 0;
  padding: 0;
  background-color: #409EFF;
  border: 0;
  color: white;
  display: flex;
  align-items: center;
}
</style>