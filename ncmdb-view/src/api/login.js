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