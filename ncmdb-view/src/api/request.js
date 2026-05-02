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