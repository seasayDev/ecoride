<template>
  <router-view></router-view>
  <childRouter />
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";
import childRouter from "./components/childRouter.vue";
import Shark from "./components/Shark.vue";

export default defineComponent({
  components: {
    childRouter,
  },
  setup() { },
});
</script>
