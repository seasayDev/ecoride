<template>
  <NavBar />
  <router-view></router-view>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

import NavBar from "./components/NavBar.vue";
import Home from '@/components/home/Home.vue'

export default defineComponent({
  name: 'App',
  components: {
    NavBar,
    Home
  },
  setup() { },
});
</script>
