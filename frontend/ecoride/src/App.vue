<template>
  <NavBar />
  <main class="page-wrap">
    <router-view v-slot="{ Component }">
      <transition name="fade" mode="out-in">
        <component :is="Component" />
      </transition>
    </router-view>
  </main>
  <Footer />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import NavBar from '@/components/navBar/NavBar.vue'
import Footer from '@/components/footer/Footer.vue'

export default defineComponent({
  name: 'App',
  components: { NavBar, Footer }
})
</script>

<style>
.page-wrap { min-height: 70vh; }
.fade-enter-from, .fade-leave-to { opacity: 0; transform: translateY(6px); }
.fade-enter-active, .fade-leave-active { transition: all .25s ease; }
</style>
