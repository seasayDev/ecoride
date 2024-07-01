<template>
    <div class="card" style="width: 18rem;">
        <img class="card-img-top" :src="getImageSrc(scooter.image.data)" alt="scooter 1">
        <div class="card-body">
            <h5 class="card-title">{{ scooter.name }}</h5>
            <p class="card-text">{{ scooter.location.name }} </p>
            <a href="#" class="btn btn-primary">Reserver</a>
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
    setup(props, { emit }) {
        const getImageSrc = (imageData: string) => {
            return `data:image/webp;base64,${imageData}`;
        };

        return {
            getImageSrc
        }

    },
})
</script>
<style scoped>
.card {
    margin: 1rem;
}
</style>
