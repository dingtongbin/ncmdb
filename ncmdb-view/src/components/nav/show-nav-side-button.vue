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