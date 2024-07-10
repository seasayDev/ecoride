<template>
    <div class="card" :class="{ 'card-disabled': scooter.qte === 0 }" style="width: 18rem;">
        <div class="status-bar" :class="statusClass">
            Trottinettes disponibles: {{ scooter.qte }}
        </div>
        <img class="card-img-top" :src="getImageSrc(scooter.image.data)" alt="scooter 1">
        <div class="card-body">
            <h5 class="card-title">{{ scooter.name }}</h5>
            <p class="card-text">{{ scooter.location.name }}</p>
            <button @click="reserve" class="btn btn-primary" :disabled="scooter.qte === 0">Reserver</button>
            <button @click="showCommentairesModal = true" class="btn btn-secondary">Voir commentaires</button>
            
        </div>

      <CommentairesModal 
      :isVisible="showCommentairesModal" 
      :scooter="scooter" 
      @close="showCommentairesModal = false" 
    />
    </div>
</template>
  
<script lang="ts">
import { defineComponent, PropType, computed } from 'vue';
import { Trotinette } from './scooterCard';

export default defineComponent({
    props: {
        scooter: {
            type: Object as PropType<Trotinette>,
            required: true
        }
    },
    emits: ['reserve'],
    setup(props, { emit }) {
        const reserve = () => {
            emit('reserve', props.scooter);
        };

        const getImageSrc = (imageData: string) => {
            return `data:image/webp;base64,${imageData}`;
        };

        const statusClass = computed(() => {
            if (props.scooter.qte === 0) return 'status-bar-red';
            if (props.scooter.qte <= 5) return 'status-bar-orange';
            return 'status-bar-green';
        });

        return {
            getImageSrc,
            reserve,
            statusClass,
        };
    }
});

</script>
  
<style scoped>
.card {
    margin: 1rem;
    padding: 0;
}

.card-disabled {
    opacity: 0.5;
}

.status-bar {
    width: 100%;
    height: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: white;
    font-weight: bold;
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    box-sizing: border-box;
}

.status-bar-green {
    background-color: lightgreen;
}

.status-bar-orange {
    background-color: orange;
}

.status-bar-red {
    background-color: red;
}

.card-img-top {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}



.scooter-card {
  padding: 1rem;
  margin: 1rem;
  border: 1px solid #ccc;
  border-radius: 0.5rem;
  text-align: center;
}
.scooter-card img {
  width: 100%;
  height: auto;
}
.btn-group {
  display: flex;
  justify-content: space-between;
  margin-top: 0.5rem;
}
.btn {
  margin: 0.5rem;
}
.ml-auto {
  margin-left: auto;
}
</style>
  