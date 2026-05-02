import {defineStore} from 'pinia'  // 添加这行导入
import {ref} from 'vue'

export const storeSetting = defineStore('setting', () => {

    const show_side=ref(true)
    const access_token=ref('')
    const isLoginRoute=ref(false)

    return {
       show_side,
        access_token,
        isLoginRoute,

    }
})