<template>
  <nav>
    <ul>
      <li>
        <router-link to="/">Home</router-link>
      </li>
      <li>
        <router-link to="/login" v-if="!userStore.user">Connexion</router-link>
      </li>
      <li>
        <router-link v-if="userStore.user" to="/support">Support</router-link>
      </li>

      <li class="dropdown" v-if="userStore.user">
        <a href="javascript:void(0)" class="dropbtn">Mon compte</a>
        <div class="dropdown-content">
          <router-link to="/profil">Modifier Profil</router-link>
          <router-link to="/facturation">Modifier Facturation</router-link>
        </div>
      </li>

      <li>
        <router-link v-if="userStore.user" to="/aide">Aide</router-link>
      </li>


      <li>
        <router-link v-if="userStore.user" to="/" @click.prevent="deconnexion">Deconnexion</router-link>
      </li>
      <li>
        <router-link v-if="userStore.user?.session.role === 'admin'" to="/admin">Admin</router-link>
      </li>
      <li>
        <router-link v-if="userStore.user" to="/map">deplacement</router-link>
      </li>
      <li>
        <router-link v-if="userStore.user" to="/reservations">Reservations</router-link>
      </li>
    </ul>

    <span v-if="userStore.user" class="username">{{ getUserName }}</span>
  </nav>
</template>

<script lang="ts">
import { useRouter } from 'vue-router'
import { defineComponent, reactive, computed, inject } from 'vue'
import { userStore, setUser, getUserFromStorage } from '@/components/helpers/userSession'
import { LoginUser } from '../login'

export default defineComponent({
  name: 'NavBar',
  setup() {
    const loginUser = inject('loginUser') as LoginUser
    const router = useRouter()

    const state = reactive({
      user: {} as Object | null,
      userName: ''
    })

    getUserFromStorage()

    const getUserName = computed(() => {
      return userStore.user?.session.fname
    })

    const deconnexion = () => {
      loginUser.deconnexion(userStore.user?.session.id)
      setUser(null)
      router.push('/')
    }

    return {
      state,
      deconnexion,
      router,
      userStore,
      loginUser,
      getUserName
    }
  }
})
</script>

<style scoped>
nav {
  background-color: #333;
  padding: 1rem;
}

ul {
  list-style: none;
  display: flex;
  gap: 1rem;
}

li {
  display: inline;
  position: relative;
}

a {
  color: white;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}

.username {
  position: absolute;
  color: white;
  right: 33px;
  top: 16px;
}

/* Dropdown styles */
.dropdown .dropbtn {
  cursor: pointer;
  color: white;
  text-decoration: none;
  background-color: #333;
  border: none;
  padding: 0;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0, 0, 0, 0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {
  background-color: #f1f1f1;
}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown:hover .dropbtn {
  background-color: #3e8e41;
}

/* Responsive adjustments */
@media screen and (max-width: 600px) {
  ul {
    flex-direction: column;
    gap: 0;
  }

  .dropdown-content {
    position: static;
  }
}
</style>