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
