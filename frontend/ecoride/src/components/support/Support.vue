<template>
    <div class="container mt-5">
      <h1>Support Page</h1>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="supportOption" class="form-label">Support Option:</label>
          <select id="supportOption" class="form-control" v-model="state.model.supportOption">
            <option value="">Select an option</option>
            <option value="chat">Chat en direct</option>
            <option value="email">Email</option>
            <option value="phone">Téléphone</option>
          </select>
        </div>
        <div class="mb-3">
          <label for="message" class="form-label">Message:</label>
          <textarea id="message" class="form-control" v-model="state.model.message"></textarea>
        </div>
        <button type="submit" class="btn btn-dark">Submit</button>
      </form>
      <p v-if="state.confirmation">{{ state.confirmation }}</p>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive } from 'vue';
  import { SupportRequest, SupportService } from './support';
  
  export default defineComponent({
    name: 'Support',
    setup() {
      const supportService = new SupportService('/support'); // Remplacez par votre URL de backend
      const state = reactive({
        model: {} as SupportRequest,
        confirmation: ''
      });
  
      const submitForm = async () => {
        try {
          const response = await supportService.submitRequest(state.model);
          state.confirmation = response.message;
        } catch (e) {
          console.error('There was an error submitting the support request!', e);
        }
      };
  
      return {
        state,
        submitForm
      };
    },
  });
  </script>
  
  <style scoped>
  .container {
      background-color: var(--blue-light);
      padding: 20px;
      border-radius: 8px;
  }
  </style>
  