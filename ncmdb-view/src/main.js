import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router.js";
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'

const pinia=createPinia()
const app =createApp(App)

app.use(ElementPlus, {
    locale: zhCn,
})


for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
    app.component(key, component)
}

app.use(router)
app.use(pinia)

app.mount('#app')
