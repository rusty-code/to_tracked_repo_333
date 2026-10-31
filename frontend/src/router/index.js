import { createRouter, createWebHistory } from 'vue-router'

import AppLayout  from "@/layouts/AppLayout.vue";
  import Devices from "@/views/Devices.vue";
  import Scripts from "@/views/Scripts.vue"
  import Journal from "@/views/Journal.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      children: [
        {
          path: 'devices',
          component: Devices,
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
