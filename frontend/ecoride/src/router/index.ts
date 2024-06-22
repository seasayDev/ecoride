import { createRouter, createWebHistory } from 'vue-router'
import Shark from '@/components/Shark.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/shark',
      name: 'Shark',
      component: Shark
    }
  ]
})

export default router
