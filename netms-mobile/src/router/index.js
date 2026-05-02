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