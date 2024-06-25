<template>
    <div class="container">
        <div class="row">
            <ScooterCard v-for="(scooter, index) in 6" :key="index" :class="gridClass" :scooter="scooter">
            </ScooterCard>
        </div>
    </div>
</template>
<script lang="ts">
import { computed, defineComponent } from 'vue'
import ScooterCard from '../scooterCard/ScooterCard.vue'


export default defineComponent({
    components: {
        ScooterCard
    },
    setup() {
        const gridClass = computed(() => {
            return { 'col-lg-3 col-md-6 col-sm-6 col-12': true }
        })
        return {
            gridClass
        }

    },
})
</script>
<style scoped></style>
