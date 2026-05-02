import {defineStore} from 'pinia'  // 添加这行导入
import {ref} from 'vue'

export const storeSetting = defineStore('setting', () => {

    const show_login=ref(false)
    const show_register=ref(false)
    const is_login=ref(false)


    return {
        show_login,
        show_register,

    }
})