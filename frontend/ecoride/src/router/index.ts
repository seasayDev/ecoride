import { createRouter, createWebHistory } from 'vue-router'
import login from '@/components/login/Login.vue'
import register from '@/components/register/Register.vue'
import ResetPassword from '@/components/resetPassword/ResetPassword.vue'
import Home from '@/components/home/Home.vue'
import Support from '@/components/support/Support.vue'
import Profil from '@/components/profil/Profil.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'Login', component: login },
    { path: '/register', name: 'Register', component: register },
    { path: '/resetPassword', name: 'ResetPassword', component: ResetPassword },
    { path: '/', name: 'Home', component: Home },
    { path: '/support', name: 'Support', component: Support },
    {path:'/profil', name:'Profil', component: Profil}
  ]
})

export default router
