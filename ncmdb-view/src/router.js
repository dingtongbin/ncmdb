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
import login from "./view/login.vue";
import index from "./view/index.vue";
import code404 from "./view/code/code404.vue";
import contact from "./view/contact.vue";
import Infrastructure from "./view/integrated_facility/Infrastructure.vue";
import alert_ from "./view/alert/alert_.vue";
import webhook from "./view/alert/webhook.vue";
import inventory from "./view/inventory.vue";
import filem from "./view/filem.vue";
import repair from "./view/repair.vue";
import PatrolPlan from "./view/operation_affairs/PatrolPlan.vue";
import PatrolTask from "./view/operation_affairs/PatrolTask.vue";
import network_device from "./view/device/network_device.vue";
import ipam from "./view/device/ipam.vue";
import terminal from "./view/device/terminal.vue";

const router = createRouter({
    history: createWebHistory(),
    routes: [

        {
            path: '/',
            component: index,
        },  {
            path: '/login',
            component: login,
        },  {
            path: '/ipam',
            component: ipam,
        },  {
            path: '/network_device',
            component: network_device,
        },  {
            path: '/terminal',
            component: terminal,
        }, {
            path: '/Infrastructure',
            component: Infrastructure,
        },{
            path: '/alert/alert',
            component: alert_,
        },{
            path: '/filem',
            component: filem,
        },{
            path: '/alert/webhook',
            component: webhook,
        },{
            path: '/inventory',
            component: inventory,
        },{
            path: '/patrol_plan',
            component: PatrolPlan,
        },{
            path: '/patrol_task',
            component: PatrolTask,
        },{
            path: '/contact',
            component: contact,
        },  {
            path: '/repair',
            component:repair ,

        },

        {
            path: '/:pathMatch(.*)*',
            component: code404,
        }
    ]
})
// 全局前置守卫
router.beforeEach((to, from, next) => {
    // 检查是否有访问令牌（假设存储在 localStorage 中）
    const token = localStorage.getItem('access_token');

    // 如果没有令牌且不是前往登录页，则跳转到登录页
    if (!token && to.path !== '/login') {
        next('/login');
    } else {
        next(); // 允许继续导航
    }
});



export default router;