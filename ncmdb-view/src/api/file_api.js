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

// 列出目录内容
import request from "./request.js";

export const listDirectory = async (params) => {
    const response = await request.get('/api/file/list/', { params })
    return response.data
}

// 上传文件
export const uploadFiles = async (formData) => {
    const response = await request.post('/api/file/upload/', formData, {
        headers: {
            'Content-Type': 'multipart/form-data'
        }
    })
    return response.data
}

// 创建文件夹
export const createFolder = async (data) => {
    const response = await request.post('/api/file/folder/create/', data)
    return response.data
}

// 重命名
export const renameItem = async (data) => {
    const response = await request.post('/api/file/rename/', data)
    return response.data
}

// 删除
export const deleteItem = async (data) => {
    const response = await request.post('/api/file/delete/', data)
    return response.data
}

// 预览文件
export const previewFile = async (params) => {
    const response = await request.get('/api/file/preview/', { params })
    return response.data
}

// 下载文件（POST 方式，安全）
export const downloadFile = async (data) => {
    const response = await request.post('/api/file/download/', data)
    return response.data
}
