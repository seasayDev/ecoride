import { createRouter, createWebHistory } from 'vue-router'
import login from '@/components/login/Login.vue'
import register from '@/components/register/Register.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'Login', component: login },
    { path: '/register', name: 'Register', component: register }
  ]
})

export default router
