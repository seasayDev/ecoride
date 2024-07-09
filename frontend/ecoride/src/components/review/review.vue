<template>
  <div class="container mt-5">
      <form @submit.prevent="submitForm" class="review-form">
      <h2>Laisser un commentaire </h2>
      <span>Donnez votre avis sur la trottinette que vous avez louée</span>
      <div class="form-group">
        <label for="rating">Note</label>
        <input type="number" class="form-control" id="rating" min="1" max="5" v-model="state.model.rating" required>
      </div>
      <div class="form-group">
        <label for="comment">Commentaire</label>
        <textarea class="form-control" id="comment" v-model="state.model.comment" required></textarea>
      </div>
      <button type="submit" class="btn btn-primary">Soumettre</button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent, reactive, inject } from 'vue'
import type { AddReviewService, ReviewModel } from '../services/addReviewService'

export default defineComponent({
  name: "AddReview",
  setup() {
    const addReviewService = inject('addReviewService') as AddReviewService
    const state = reactive({
      model: {
        rating: 0,
        comment: '',
        scooterId: 1, // exemple statique, vous pouvez passer cet id dynamiquement
        userId: 1 // exemple statique, vous pouvez passer cet id dynamiquement
      } as ReviewModel
    })

    const submitForm = async () => {
      await addReviewService.addReview(state.model)
    }

    return {
      state,
      submitForm,
      addReviewService
    }
  },
})
</script>

<style scoped>
.review-form {
  padding: 2rem;
  background-color: var(--blue-light);
  border-radius: 0.5rem;
}

.btn {
  margin-top: 2rem;
}
</style>
