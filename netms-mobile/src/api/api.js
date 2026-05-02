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

export const API_URL="http://127.0.0.1:8000"
export const request=axios.create({
    baseURL:API_URL,
    timeout:10000
})

// 请求拦截器 - 自动添加 access_token
request.interceptors.request.use(
    config => {
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

// 登录接口
export const login = async (username, password) => {
    const response = await request.post('/api/token/', { username, password })
    return response.data
}

// 获取工单列表
export const getRepairRequests = async () => {
    const response = await request.get('/api/repair/work-order/my-list/')
    return response.data
}

// 提交工单
export const submitRepairRequest = async (data) => {
    const response = await request.post('/api/repair/work-order/create/', data)
    return response.data
}

// 获取工单详情
export const getWorkOrderDetail = async (id) => {
    const response = await request.get(`/api/repair/work-order/${id}/`)
    return response.data
}

// 提交评价
export const submitEvaluation = async (id, data) => {
    const response = await request.post(`/api/repair/work-order/${id}/evaluation/`, data)
    return response.data
}

// 修改密码接口
export const changePassword = async (data) => {
    const response = await request.post('/api/change_password/', data)
    return response.data
}
export const getUserInfo = async () => {
    const response = await request.get('/api/user_info/')
    return response.data
}

export default request
