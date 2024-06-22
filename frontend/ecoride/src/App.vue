<template>
  <NavBar />
  <router-view></router-view>
  <!-- <childRouter /> -->
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import childRouter from "./components/childRouter.vue";
import Shark from "./components/Shark.vue";
import NavBar from "./components/NavBar.vue";

export default defineComponent({
  components: {
    childRouter,
    NavBar
  },
  setup() { },
});
</script>
