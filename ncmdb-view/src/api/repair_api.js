
// 获取工单详情

import request from "./request.js";

export const getWorkOrderDetail = async (id) => {
    const response = await request.get(`/api/repair/work-order/${id}/`)
    return response.data
}

// 提交评价
export const submitEvaluation = async (id, data) => {
    const response = await request.post(`/api/repair/work-order/${id}/evaluation/`, data)
    return response.data
}

// ============ 网络工程师专用 API ============

// 获取工单列表（带筛选和分页）
export const getEngineerWorkOrders = async (params) => {
    const response = await request.get('/api/repair/engineer/work-orders/', { params })
    return response.data
}

// 接单
export const acceptWorkOrder = async (id) => {
    const response = await request.post(`/api/repair/engineer/work-order/${id}/accept/`)
    return response.data
}

// 提交处理结果
export const submitWorkOrderResult = async (id, data) => {
    const response = await request.post(`/api/repair/engineer/work-order/${id}/submit-result/`, data)
    return response.data
}

