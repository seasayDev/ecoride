<template>
  <NavBar />
  <router-view></router-view>
  <!-- <childRouter /> -->
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

import NavBar from "./components/NavBar.vue";

export default defineComponent({
  components: {
    NavBar
  },
  setup() { },
});
</script>
