<template>
  <div>
    <div class="card" :class="{ 'card-disabled': scooter.qte === 0 }" style="width: 18rem;">
      <div class="status-bar" :class="statusClass">
        Trottinettes disponibles: {{ scooter.qte }}
      </div>
      <img class="card-img-top" :src="getImageSrc(scooter.image.data)" alt="scooter 1">
      <div class="card-body">
        <h5 class="card-title">{{ scooter.name }}</h5>
        <p class="card-text">{{ scooter.location.name }}</p>
        <button @click="reserve" class="btn btn-primary" :disabled="scooter.qte === 0">Reserver</button>
        <br />
        <button @click="showCommentaires" class="btn btn-secondary mt-2">Voir commentaires</button>
      </div>
    </div>
    
    <CommentairesModal 
      :isVisible="showCommentairesModal" 
      :scooter="scooter" 
      @close="hideCommentaires" 
    />
  </div>
</template>

<script lang="ts">
import { defineComponent, ref, computed } from 'vue';
import CommentairesModal from '@/components/review/review.vue'; // Ajuster le chemin d'importation
import { Trotinette } from './scooterCard';

export default defineComponent({
  components: {
    CommentairesModal
  },
  props: {
    scooter: {
      type: Object as PropType<Trotinette>,
      required: true
    }
  },
  emits: ['reserve', 'update-quantity'],
  setup(props, { emit }) {
    const showCommentairesModal = ref(false);

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

    const showCommentaires = () => {
      showCommentairesModal.value = true;
    };

    const hideCommentaires = () => {
      showCommentairesModal.value = false;
    };

    return {
      showCommentairesModal,
      getImageSrc,
      reserve,
      statusClass,
      showCommentaires,
      hideCommentaires
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
  border-top-right-radius: 0;
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

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
}

.mt-2 {
  margin-top: 0.5rem; /* Classe pour ajouter un espace au dessus du bouton Voir commentaires */
}
</style>
