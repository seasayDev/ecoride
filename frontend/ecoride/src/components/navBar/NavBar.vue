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
            <li>
                <router-link v-if="userStore.user" to="/profil">Profil</router-link>
            </li>

            <li>
                <router-link v-if="userStore.user" to="/facturation">Facturation</router-link>
            </li>


            <!-- <li>
                <router-link v-if="userStore.user" to="/payement">Payement</router-link>
            </li> -->

            <li>
                <router-link v-if="userStore.user" to="/aide">Aide</router-link>
            </li>

            <li>
                <router-link v-if="userStore.user" to="/" @click.prevent="deconnexion">Deconnexion</router-link>
            </li>
            <li>
                <router-link v-if="userStore.user" to="/admin">Admin</router-link>
            </li>
            <li>
                <router-link v-if="userStore.user" to="/map">deplacement</router-link>
            </li>
        </ul>

        <span v-if="userStore.user" class="username">{{ getUserName }}</span>

    </nav>
</template>
  
<script lang="ts">
import { useRouter } from "vue-router";
import { defineComponent, onMounted, reactive, watch, inject, computed } from 'vue';
import { userStore, setUser, getUserFromStorage } from "@/components/helpers/userSession";
import { LoginUser } from '../login';
export default defineComponent({
    name: 'NavBar',
    setup() {
        const loginUser = inject('loginUser') as LoginUser;
        const router = useRouter();

        const state = reactive({
            user: {} as Object | null,
            userName: ''
        })

        getUserFromStorage();

        const getUserName = computed(() => { return userStore.user?.session.fname })

        const deconnexion = () => {
            loginUser.deconnexion(userStore.user?.session.id)
            setUser(null);
            router.push("/")
        }


        return {
            state,
            deconnexion,
            router,
            userStore,
            loginUser,
            getUserName,

        }
    }
});
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
</style>
  