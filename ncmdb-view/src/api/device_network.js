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
