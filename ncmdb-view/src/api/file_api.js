
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
