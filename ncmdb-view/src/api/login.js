import axios from "axios";
import {ElMessage} from "element-plus";
import {API_URL, request} from "./request.js";

export const login = async (username, password) => {
    try {
        const res = await axios.post(API_URL+'/api/token/', {
            username: username,
            password: password
        })
        console.log( res)
        return res.data
    } catch (e) {
        ElMessage.error(e)
    }
}
// 获取当前登录用户信息
export const getUserInfo = async () => {
    try {
        const res = await request.get(API_URL+'/api/user_info/')
        return res.data
    } catch (e) {
        console.error('获取用户信息失败:', e)
        throw e
    }
}