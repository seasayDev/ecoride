<template>
    <nav>
        <ul>
            <li>
                <router-link to="/">Home</router-link>
            </li>
            <li>
                <router-link to="/login">Connexion</router-link>
            </li>
            <li>
                <router-link to="/login">Deconnexion</router-link>
            </li>
        </ul>
    </nav>
</template>
  
<script lang="ts">
import { defineComponent } from 'vue';

export default defineComponent({
    name: 'NavBar'
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
</style>
  