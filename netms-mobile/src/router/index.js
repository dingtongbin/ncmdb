import {createRouter, createWebHistory} from "vue-router";

import login from "../view/login.vue";

import home from "../view/home.vue";
import networkerhmoe from "../view/networkerhmoe.vue";
import not404 from "../view/not404.vue";
import WorkOrderDetail from "../view/WorkOrderDetail.vue";


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/login",
            name: "",
            component: login,
        },{
            path: "/",
            name: "",
            component: home,
        }, {
            path: "/home",
            name: "",
            component: home,
        }, {
            path: "/workorder/:id",
            name: "workOrderDetail",
            component: WorkOrderDetail,
        },{
            path: "/networkerhmoe",
            name: "",
            component: networkerhmoe,
        }, {
            path: '/:pathMatch(.*)*',
            component: not404,
        }
    ]
})
// ... existing code ...



// 路由守卫
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('access_token')
    if (to.path !== '/login' && !token) {
        next('/login')
    } else if (to.path === '/login' && token) {
        next('/home')
    } else {
        next()
    }
})

// ... existing code ...

export default router;