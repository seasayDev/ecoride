import { createRouter, createWebHistory } from 'vue-router'
import login from '@/components/login/Login.vue'
import register from '@/components/register/Register.vue'
import ResetPassword from '@/components/resetPassword/ResetPassword.vue'
import Home from '@/components/home/Home.vue'
import Support from '@/components/support/Support.vue'
import Profil from '@/components/profil/Profil.vue'
import EditProfil from '@/components/editProfil/EditProfil.vue'
import admin from '@/components/admin/admin.vue'
import Aide from '@/components/aide/Aide.vue'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'Login', component: login },
    { path: '/register', name: 'Register', component: register },
    { path: '/resetPassword', name: 'ResetPassword', component: ResetPassword },
    { path: '/', name: 'Home', component: Home },
    { path: '/support', name: 'Support', component: Support },
    {path:'/profil', name:'Profil', component: Profil},
    {path:'/editProfil', name:'EditProfil', component: EditProfil},
    { path: '/admin', name: 'admin', component: admin },
    {path:'/aide', name:'Aide', component: Aide},

  ]
})

export default router
