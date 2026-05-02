import { createApp } from 'vue'
import './style.css'
import App from './App.vue'
import router from "./router/index.js";
import 'element-plus/dist/index.css' // 确保引入样式
import axios from 'axios'
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'
import zhCn from 'element-plus/es/locale/lang/zh-cn'
import {createPinia} from "pinia";
const pinia=createPinia()
const app = createApp(App)

app.use(ElementPlus, {
    locale: zhCn,
})
// 导入vue路由
app.use(pinia)
app.use(router)
app.mount('#app')
