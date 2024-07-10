<template>
  <div class="container mt-5">
    <h2>Commentaires pour la trottinette {{ scooterId }}</h2>
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
        <input type="number" v-model="newComment.rating" class="form-control" id="rating" min="1" max="5" required>
      </div>
      <div class="form-group">
        <label for="comment">Commentaire</label>
        <textarea v-model="newComment.comment" class="form-control" id="comment" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary mt-3">Soumettre</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRoute } from 'vue-router';

export default defineComponent({
  name: 'Commentaires',
  setup() {
    const route = useRoute();
    const scooterId = route.params.scooterId;
    console.log("Scooter ID:", scooterId);

    return {
      scooterId
    };
  },
  data() {
    return {
      commentaires: [
        { id: 1, user: 'Utilisateur 1', rating: 4, comment: 'Très bien!' },
        { id: 2, user: 'Utilisateur 2', rating: 5, comment: 'Parfait!' }
      ],
      newComment: {
        rating: 0,
        comment: ''
      }
    };
  },
  methods: {
    submitComment() {
      const newComment = {
        id: this.commentaires.length + 1,
        user: 'Moi',
        rating: this.newComment.rating,
        comment: this.newComment.comment
      };
      this.commentaires.push(newComment);
      this.newComment.rating = 0;
      this.newComment.comment = '';
    }
  }
});
</script>

<style scoped>
.container {
  padding: 2rem;
}
</style>
