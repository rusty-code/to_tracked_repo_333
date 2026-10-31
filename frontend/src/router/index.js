import { createRouter, createWebHistory } from 'vue-router'

import AppLayout  from "@/layouts/AppLayout.vue";
  import Devices from "@/views/Devices.vue";
  import Scripts from "@/views/Scripts.vue"
  import Journal from "@/views/Journal.vue";
  import Device from "@/views/Device.vue";
  
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: 'devices',
          component: Device,
        },
        {
          path: 'scripts',
          component: Scripts,
        },
        {
          path: 'journal',
          component: Journal,
        },
      ]
    },
  ],
})

export default router
