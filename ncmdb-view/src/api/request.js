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
import axios from "axios";
import {storeSetting} from "../pinia/store_setting.js";

export const API_URL="http://127.0.0.1:8000"
export const request=axios.create({
    baseURL:API_URL,
    timeout:10000
})
// 请求拦截器 - 自动添加access_token
request.interceptors.request.use(
    config => {
        // 暂时不启用
        // const userStore = storeSetting()
        // const token = userStore.access_token
        const token = localStorage.getItem('access_token')
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }

        return config
    },
    error => {
        return Promise.reject(error)
    }
)
export default  request