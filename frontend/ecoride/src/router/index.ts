import { createRouter, createWebHistory } from 'vue-router'
import Shark from '@/components/Shark.vue'
import login from '@/components/login/Login.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/shark',
      name: 'Shark',
      component: Shark
    },
    { path: '/login', name: 'Login', component: login }
  ]
})

export default router
