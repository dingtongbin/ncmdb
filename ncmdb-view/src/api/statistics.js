import {ElMessage} from "element-plus";
import {request} from "./request.js";

export const getAlertStatistics = async () => {
    try {
        const res = await request.get('/api/statistics/')
        console.log(res.data)
        return res.data
    } catch (e) {
        ElMessage.error('获取统计数据失败：' + e.message)
        throw e
    }
}
