<template>
    <div class="container mt-5">
      <div v-if="state.successMessage" class="alert alert-success" role="alert">
        {{ state.successMessage }}
      </div>
      <h2 class="mb-4">Modifier les informations de facturation</h2>
      <form @submit.prevent="updateFacturation">
        <div class="row mb-3" hidden>
          <div class="col-md-6">
            <label for="montant" class="form-label">Montant :</label>
            <input type="number" class="form-control" id="montant" v-model="state.facturation.montant" required>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col-md-6">
            <label for="nom" class="form-label">Nom :</label>
            <input type="text" class="form-control" id="nom" v-model="state.facturation.nom" required>
          </div>
          <div class="col-md-6">
            <label for="prenom" class="form-label">Prénom :</label>
            <input type="text" class="form-control" id="prenom" v-model="state.facturation.prenom" required>
          </div>
        </div>
        <div class="mb-3">
          <label for="adresse" class="form-label">Adresse :</label>
          <input type="text" class="form-control" id="adresse" v-model="state.facturation.adresse" required>
        </div>
        <div class="row mb-3">
          <div class="col-md-4">
            <label for="ville" class="form-label">Ville :</label>
            <input type="text" class="form-control" id="ville" v-model="state.facturation.ville" required>
          </div>
          <div class="col-md-4">
            <label for="province" class="form-label">Province :</label>
            <input type="text" class="form-control" id="province" v-model="state.facturation.province" required>
          </div>
          <div class="col-md-4">
            <label for="codePostal" class="form-label">Code postal :</label>
            <input type="text" class="form-control" id="codePostal" v-model="state.facturation.codePostal" required>
          </div>
        </div>
        <div class="mb-3">
          <label for="telephone" class="form-label">Téléphone :</label>
          <input type="tel" class="form-control" id="telephone" v-model="state.facturation.telephone" required>
        </div>
        <button type="submit" class="btn btn-primary">Mettre à jour</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, inject, onMounted } from 'vue';
  import type { FacturationInfo } from '../facturation/facturation';
  import { FacturationService } from '../facturation/facturation';
  import { userStore, getUserFromStorage } from "@/components/helpers/userSession";
  
  export default defineComponent({
    name: 'EditFacturation',
    setup() {
      const facturationService = inject('facturationService') as FacturationService;
  
      const state = reactive({
        facturation: {
          montant: 20,
          nom: '',
          prenom: '',
          adresse: '',
          ville: '',
          province: '',
          codePostal: '',
          telephone: '',
        } as FacturationInfo,
        error: false,
        successMessage: '',
      });
  
      onMounted(async () => {
        try {
          getUserFromStorage();
          const id_user = userStore.user?.session.id_user;
  
          if (id_user) {
            const data = await facturationService.getFacturation(id_user);
            state.facturation = data;
          } else {
            state.error = true;
            console.error('Erreur : Utilisateur non connecté');
          }
        } catch (error) {
          console.error('Erreur lors du chargement des informations de facturation:', error);
          state.error = true;
        }
      });
  
      const updateFacturation = async () => {
        try {
          getUserFromStorage();
          const id_user = userStore.user?.session.id_user;
  
          if (id_user) {
            await facturationService.updateFacturation(id_user, state.facturation);
            state.successMessage = 'Informations de facturation mises à jour avec succès';
            setTimeout(() => {
              state.successMessage = '';
            }, 9000);
          } else {
            state.error = true;
            console.error('Erreur : Utilisateur non connecté');
          }
        } catch (error) {
          console.error('Erreur lors de la mise à jour des informations de facturation:', error);
          state.error = true;
        }
      };
  
      return {
        state,
        updateFacturation,
      };
    },
  });
  </script>
  
  <style scoped>
  h2 {
    text-align: center;
    text-decoration: double;
    text-transform: uppercase;
  }
  
  .container {
    background-color: var(--blue-light);
    padding: 20px;
    border-radius: 8px;
    color: #fff;
  }
  
  .form-label {
    font-weight: bold;
  }
  
  .form-control {
    background-color: rgba(255, 255, 255, 0.1);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: #fff;
  }
  
  .form-control:focus {
    background-color: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.5);
    color: #fff;
    box-shadow: 0 0 0 0.2rem rgba(255, 255, 255, 0.25);
  }
  
  .btn-primary {
    background-color: #007bff;
    border-color: #007bff;
  }
  
  .btn-primary:hover {
    opacity: 0.9;
  }
  
  .alert-success {
    background-color: #d4edda;
    border-color: #c3e6cb;
    color: #155724;
  }
  </style>