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