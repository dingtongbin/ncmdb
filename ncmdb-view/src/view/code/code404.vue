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

import router from "../../router.js";
</script>

<template>
  <div class="container">
    <div class="div1">
      <div class="div2">404</div>
      <div class="div3">系统未找到页面或页面不存在</div>
      <div class="div4">
        <button @click="router.back()">返回上一页</button>
        <button @click="router.push('/')">返回首页</button>

      </div>

    </div>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  justify-content: center;
  width: 100%;
  height: 100%
}

.div1 {
  width: 400px;
  height: 400px;
  border: black solid 2px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  border-radius: 10px;
}

.div2 {
  width: 100%;
  font-size: 4rem;
  font-weight: bold;
  display: flex;
  justify-content: center;
}
.div3{
  width: 100%;
  display: flex;
  justify-content: center;
}
.div4{
  width: 100%;
  display: flex;
  justify-content: center;
}
.div4>button{
  border: black solid 2px;
  border-radius: 5px;
  margin-right: 10px;
  height: 40px;
  width: 100px;
  font-weight: bold;
  background-color: white;
  cursor: pointer;
}
.div4>button:active{
  background-color: rgba(191, 191, 191, 0.52);
}
</style>