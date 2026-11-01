import { createRouter, createWebHistory } from 'vue-router'

import AppLayout  from "@/layouts/AppLayout.vue";
  import Scripts from "@/views/Scripts.vue"
  import Journal from "@/views/Journal.vue";
  import Device from "@/views/Device.vue";
  import Service from "@/views/Service.vue";
  import Vet from "@/views/Vet.vue";
  import Emulators from "@/views/Emulators.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: AppLayout,
      redirect: '/service',
      children: [
        {
          path: 'service',
          component: Service,
        },
        {
          path: 'vet',
          component: Vet,
        },
        {
          path: 'emulators',
          component: Emulators,
        },
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
