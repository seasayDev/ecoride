<template>
  <div class="modal" v-if="isVisible" @click.self="closeModal">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Commentaires pour {{ scooter.name }}</h5>
          <button type="button" class="btn-close" @click="closeModal"></button>
        </div>
        <div class="modal-body">
          <ul v-if="commentaires.length">
            <li v-for="commentaire in commentaires" :key="commentaire.id">
              <p><strong>{{ commentaire.user }}</strong>: {{ commentaire.comment }}</p>
              <p>Note: {{ commentaire.rating }}</p>
            </li>
          </ul>
          <p v-else>Aucun commentaire pour le moment.</p>
          <form @submit.prevent="submitComment">
            <div class="form-group">
              <label for="rating">Note</label>
              <input type="number" v-model="newComment.rating" class="form-control" id="rating" min="0" max="5" required>
            </div>
            <div class="form-group">
              <label for="comment">Commentaire</label>
              <textarea v-model="newComment.comment" class="form-control" id="comment" required></textarea>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Soumettre</button>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, PropType, ref } from 'vue';
import { Trotinette } from '../scooterCard/scooterCard';

export default defineComponent({
  props: {
    isVisible: {
      type: Boolean as PropType<boolean>,
      required: true
    },
    scooter: {
      type: Object as PropType<Trotinette>,
      required: true
    }
  },
  emits: ['close'],
  setup(props, { emit }) {
    const commentaires = ref([
      { id: 1, user: 'Utilisateur 1', rating: 4, comment: 'Très bien!' },
      { id: 2, user: 'Utilisateur 2', rating: 5, comment: 'Parfait!' }
    ]);

    const newComment = ref({
      rating: 0,
      comment: ''
    });

    const closeModal = () => {
      emit('close');
    };

    const submitComment = () => {
      const newCommentData = {
        id: commentaires.value.length + 1,
        user: 'Moi',
        rating: newComment.value.rating,
        comment: newComment.value.comment
      };
      commentaires.value.push(newCommentData);
      newComment.value.rating = 0;
      newComment.value.comment = '';
    };

    return {
      commentaires,
      newComment,
      closeModal,
      submitComment
    };
  }
});
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  z-index: 1000;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-dialog {
  background-color: #fff;
  padding: 20px;
  border-radius: 4px;
  width: 600px; /* Définir une largeur fixe */
  max-width: 80%; /* Optionnel : Pour s'assurer que la modale reste responsive */
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
}
</style>
