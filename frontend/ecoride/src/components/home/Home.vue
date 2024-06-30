<template>
    <div class="container">
        <div class="row">
            <ScooterCard v-for="(scooter, index) in state.scooters" :key="index" :class="gridClass" :scooter="scooter">
            </ScooterCard>
        </div>
    </div>
</template>
<script lang="ts">
import { computed, defineComponent, inject, onMounted, reactive } from 'vue'
import ScooterCard from '../scooterCard/ScooterCard.vue'
import { GetTrotinettes, Trotinette } from '../admin'

export default defineComponent({
    components: {
        ScooterCard
    },
    setup() {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const gridClass = computed(() => {
            return { 'col-lg-3 col-md-6 col-sm-6 col-12': true }
        })
        const state = reactive({
            scooters: {} as Array<Trotinette>
        })
        onMounted(async () => {
            state.scooters = await trotinettes.getTrotinettes()
        })
        return {
            gridClass,
            trotinettes,
            state
        }

    },
})
</script>
<style scoped></style>
