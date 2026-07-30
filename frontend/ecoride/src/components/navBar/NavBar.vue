<template>
  <header class="topbar bg-white border-bottom">
    <div class="container d-flex align-items-center justify-content-between h-100">
      <router-link to="/" class="brand">
        <span class="brand-dot"></span>
        EcoRide
      </router-link>
      <nav class="nav">
        <router-link v-if="!userStore.user" to="/login">Connexion</router-link>
        <template v-else>
          <router-link to="/" class="me-3">Accueil</router-link>
          <router-link to="/reservations" class="me-3">Réservations</router-link>
          <router-link to="/aide" class="me-3">Aide</router-link>
          <router-link to="/support" class="me-3">Support</router-link>
          <span class="username me-3">{{ userStore.user?.session.fname }}</span>
          <a href="javascript:void(0)" @click.prevent="deconnexion">Déconnexion</a>
        </template>
      </nav>
    </div>
  </header>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useRouter } from 'vue-router'
import { LoginUser } from '../login/login';
import { userStore, setUser } from '@/components/helpers/userSession'

export default defineComponent({
  name: 'NavBar',
  setup() {
    const router = useRouter()
    const loginUser = new LoginUser('http://127.0.0.1:5000')

    const deconnexion = async () => {
      await loginUser.deconnexion(userStore.user?.session.id)
      setUser(null)
      router.push('/')
    }
    return { userStore, deconnexion }
  }
})
</script>

<style scoped>
.topbar { position: sticky; top: 0; z-index: 1030; height: 64px; }
.brand {
  font-weight: 800; letter-spacing: -0.2px; color: #16a34a; text-decoration: none;
  display: inline-flex; align-items: center; gap: 8px;
}
.brand-dot {
  width: 18px; height: 18px; background: #16a34a; border-radius: 999px; display: inline-block;
}
.nav {
  display: flex; align-items: center; gap: 12px;
}
.nav a {
  color: #1f2937; text-decoration: none; font-weight: 500; padding: 6px 8px; border-radius: 0.5rem;
}
.nav a:hover { background-color: #f3f4f6; color: #16a34a; }
.username { color: #374151; font-weight: 600; }
</style>
