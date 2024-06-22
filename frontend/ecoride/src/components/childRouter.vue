<template>
    <button type="button" class="btn btn-primary" @click="navigateToShark">
        GO to shark
    </button>
</template>
<script lang="ts">
import { defineComponent } from "vue";
import { useRouter } from "vue-router";
export default defineComponent({
    setup() {
        const router = useRouter();
        const navigateToShark = () => {
            router.push("/shark");
        };
        return {
            navigateToShark,
        };
    },
});
</script>
  