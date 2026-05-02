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
import {ElMessage} from "element-plus";
import {request} from "./request.js";
export const networkList=async(page,page_size)=>{
    try {
        const res=await request.get(`/api/device/network/?page=${page}&page_size=${page_size}`)
        return res.data
    }catch (e){
        ElMessage.error( e)
    }
}
export const networkGet=async(id)=>{
    try {
        const res=await request.get('/api/device/network/'+id)
        return res.data
    }catch (e){
        ElMessage.error( e)
    }
}
export const networkCreate=async(data)=>{
    try {
        const res=await request.post('/api/device/network/', data)
        ElMessage.success('添加成功')
    }catch (e){
        ElMessage.error( e)
    }
}
export const networkPatch=async(id,data)=>{
    try {
        const res=await request.patch('/api/device/network/'+id, data)
        ElMessage.success('更新成功')
    }catch (e){
        ElMessage.error( e)
    }
}
export const networkDelete=async(id)=>{
    try {
        const res=await request.delete('/api/device/network/'+id)
        ElMessage.success('删除成功')
    }catch (e){
        ElMessage.error( e)
    }
}
