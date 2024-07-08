<template>
    <div class="container mt-5">
      <div v-if="state.successMessage" class="alert alert-success" role="alert">
        {{ state.successMessage }}
      </div>
      <div v-if="state.error" class="alert alert-danger" role="alert">
        {{ state.errorMessage }}
      </div>
      <h2 class="mb-4">Paiement par carte de crédit</h2>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="amount" class="form-label">Montant :</label>
          <input
            type="number"
            class="form-control"
            id="amount"
            v-model="state.form.amount"
            required
            placeholder="Entrez le montant"
          >
        </div>
  
        <div class="mb-3">
          <label for="card-number" class="form-label">Numéro de carte :</label>
          <input
            type="text"
            class="form-control"
            id="card-number"
            v-model="state.form.cardNumber"
            required
            placeholder="1234 5678 9012 3456"
            maxlength="19"
            @input="formatCardNumber"
          >
        </div>
  
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="expiry" class="form-label">Date d'expiration :</label>
            <input
              type="text"
              class="form-control"
              id="expiry"
              v-model="state.form.expiry"
              required
              placeholder="MM/AA"
              maxlength="5"
              @input="formatExpiry"
            >
          </div>
          <div class="col-md-6">
            <label for="cvv" class="form-label">CVV :</label>
            <input
              type="text"
              class="form-control"
              id="cvv"
              v-model="state.form.cvv"
              required
              placeholder="123"
              maxlength="3"
            >
          </div>
        </div>
  
        <div class="mb-3">
          <label for="card-name" class="form-label">Nom sur la carte :</label>
          <input
            type="text"
            class="form-control"
            id="card-name"
            v-model="state.form.cardName"
            required
            placeholder="Nom complet"
          >
        </div>
  
        <button type="submit" class="btn btn-primary">Payer</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject, reactive } from 'vue';
  import type { PaymentForm } from './payement';
  import { PaymentService } from './payement';
  import axios from 'axios';
  
  export default defineComponent({
    name: 'Payement',
    setup() {
      const paymentService = inject('paymentService') as PaymentService;
      const state = reactive({
        form: {} as PaymentForm,
        error: false,
        errorMessage: '',
        successMessage: ''
      });
      
      


      const submitForm = async () => {
        try {
          const response = await paymentService.processPayment(state.form);
          console.log("PAYMENT", response);
          state.successMessage = 'Paiement réussi!';
          state.error = false;
          state.errorMessage = '';
          // Réinitialiser le formulaire ici si nécessaire
          state.form = {} as PaymentForm;
        } catch (error) {
          state.error = true;
          state.successMessage = '';
          if (axios.isAxiosError(error) && error.response) {
            state.errorMessage = error.response.data.error || 'Une erreur est survenue lors du paiement';
          } else {
            state.errorMessage = 'Une erreur est survenue lors du paiement';
          }
        }
      };
  
      const formatCardNumber = (e: Event) => {
        const input = e.target as HTMLInputElement;
        let value = input.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        let formattedValue = '';
        for (let i = 0; i < value.length; i++) {
          if (i % 4 === 0 && i > 0) formattedValue += ' ';
          formattedValue += value[i];
        }
        state.form.cardNumber = formattedValue;
      };
  
      const formatExpiry = (e: Event) => {
        const input = e.target as HTMLInputElement;
        let value = input.value.replace(/\s+/g, '').replace(/[^0-9]/gi, '');
        if (value.length > 2) {
          state.form.expiry = value.slice(0, 2) + '/' + value.slice(2);
        } else {
          state.form.expiry = value;
        }
      };
  
      return {
        state,
        submitForm,
        formatCardNumber,
        formatExpiry
      };
    }
  });
  </script>
  
  <style scoped>
  .container {
    background-color: var(--blue-light);
    padding: 20px;
    border-radius: 8px;
  }
  </style>