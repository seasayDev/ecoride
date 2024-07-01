<template>
    <div class="card" style="width: 18rem;">
        <img class="card-img-top" src="../../images/scooter1.webp" alt="scooter 1">
        <div class="card-body">
            <h5 class="card-title">{{ scooter.name }}</h5>
            <p class="card-text">{{ scooter.location.name }} </p>
            <button @click="reserve" class="btn btn-primary">Reserver</button>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, PropType } from 'vue'
import { Trotinette } from './scooterCard';

export default defineComponent({
    props: {
        scooter: {
            type: {} as PropType<Trotinette>,
            required: true
        }
    },
    emits: ['reserve'],
    setup(props, { emit }) {
        const reserve = () => {
            emit('reserve', props.scooter);
        };

        return {
            reserve
        };
    },
})
</script>
<style scoped>
.card {
    margin: 1rem;
}
</style>
