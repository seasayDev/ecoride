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
import Map from '@/components/map/Map.vue'
import Payement from '@/components/payement/Payement.vue'
import ReservationDetails from '@/components/reservationDetails/ReservationDetails.vue'
import ReservationConfirmed from '@/components/reservationDetails/ReservationConfirmed.vue'
import Promotions from '@/components/promotions/promotion.vue' // Importation du composant Promotions

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/login', name: 'Login', component: login },
    { path: '/register', name: 'Register', component: register },
    { path: '/resetPassword', name: 'ResetPassword', component: ResetPassword },
    { path: '/', name: 'Home', component: Home },
    { path: '/support', name: 'Support', component: Support },
    { path: '/profil', name: 'Profil', component: Profil },
    { path: '/editProfil', name: 'EditProfil', component: EditProfil },
    { path: '/admin', name: 'admin', component: admin },
    { path: '/aide', name: 'Aide', component: Aide },
    { path: '/map', name: 'Map', component: Map },
    { path: '/payement', name: 'Payement', component: Payement },
    { path: '/promotions', name: 'Promotions', component: Promotions, meta: { requiresAuth: true } },
    { path: '/reservation-details', name: 'ReservationDetails', component: ReservationDetails },
    { path: '/reservation-confirmed', name: 'ReservationConfirmed', component: ReservationConfirmed }
  ]
})

export default router
