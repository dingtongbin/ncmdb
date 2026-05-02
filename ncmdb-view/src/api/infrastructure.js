
// 获取设备间列表
import request from "./request.js";

export const getEquipmentRooms = (params) => {
    return request({
        url: '/api/integrated_facility/equipment-rooms/',
        method: 'get',
        params
    })
}

// 创建设备间
export const createEquipmentRoom = (data) => {
    return request({
        url: '/api/integrated_facility/equipment-rooms/',
        method: 'post',
        data
    })
}

// 更新设备间
export const updateEquipmentRoom = (id, data) => {
    return request({
        url: `/api/integrated_facility/equipment-rooms/${id}/`,
        method: 'patch',
        data
    })
}

// 删除设备间
export const deleteEquipmentRoom = (id) => {
    return request({
        url: `/api/integrated_facility/equipment-rooms/${id}/`,
        method: 'delete'
    })
}

// 获取机柜列表
export const getRacks = (params) => {
    return request({
        url: '/api/integrated_facility/racks/',
        method: 'get',
        params
    })
}

// 创建机柜
export const createRack = (data) => {
    return request({
        url: '/api/integrated_facility/racks/',
        method: 'post',
        data
    })
}

// 更新机柜
export const updateRack = (id, data) => {
    return request({
        url: `/api/integrated_facility/racks/${id}/`,
        method: 'patch',
        data
    })
}

// 删除机柜
export const deleteRack = (id) => {
    return request({
        url: `/api/integrated_facility/racks/${id}/`,
        method: 'delete'
    })
}

// 获取基础设施设备列表
export const getInfrastructureEquipment = (params) => {
    return request({
        url: '/api/integrated_facility/infrastructure-equipment/',
        method: 'get',
        params
    })
}

// 创建基础设施设备
export const createInfrastructureEquipment = (data) => {
    return request({
        url: '/api/integrated_facility/infrastructure-equipment/',
        method: 'post',
        data
    })
}

// 更新基础设施设备
export const updateInfrastructureEquipment = (id, data) => {
    return request({
        url: `/api/integrated_facility/infrastructure-equipment/${id}/`,
        method: 'patch',
        data
    })
}

// 删除基础设施设备
export const deleteInfrastructureEquipment = (id) => {
    return request({
        url: `/api/integrated_facility/infrastructure-equipment/${id}/`,
        method: 'delete'
    })
}

// 获取设备详情
export const getInfrastructureEquipmentDetail = (id) => {
    return request({
        url: `/api/integrated_facility/infrastructure-equipment/${id}/`,
        method: 'get'
    })
}

// 获取连接信息列表
export const getConnections = (params) => {
    return request({
        url: '/api/integrated_facility/connections/',
        method: 'get',
        params
    })
}

// 创建连接
export const createConnection = (data) => {
    return request({
        url: '/api/integrated_facility/connections/',
        method: 'post',
        data
    })
}

// 更新连接
export const updateConnection = (id, data) => {
    return request({
        url: `/api/integrated_facility/connections/${id}/`,
        method: 'patch',
        data
    })
}

// 删除连接
export const deleteConnection = (id) => {
    return request({
        url: `/api/integrated_facility/connections/${id}/`,
        method: 'delete'
    })
}
