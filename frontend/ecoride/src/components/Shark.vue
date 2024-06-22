<template>
    <h1>{{ state.msg }}</h1>
</template>
  
<script lang="ts">
import { defineComponent, onMounted, reactive } from "vue";
import axios from "axios";
export default defineComponent({
    setup() {
        const state = reactive({
            msg: "",
        });

        onMounted(() => getResponse());
        const getResponse = async () => {
            try {
                const response = await axios.get("http://127.0.0.1:5000/shark");

                state.msg = response.data;
            } catch (error) {
                return "data not found";
            }
        };
        return {
            state,
            getResponse,
        };
    },
});
</script>
  