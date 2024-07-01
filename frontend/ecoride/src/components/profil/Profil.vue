<template>
    <div class="container mt-5">
      <div class="alert alert-danger" role="alert" v-if="state.error">
        Erreur lors de la récupération du profil utilisateur!
      </div>
      <div v-if="state.profile">
        <h2>Profil Utilisateur</h2>
        <div class="profile-card">
          <div class="profile-item">
            <label>Prénom:</label>
            <span>{{ state.profile.firstName }}</span>
          </div>
          <div class="profile-item">
            <label>Nom:</label>
            <span>{{ state.profile.lastName }}</span>
          </div>
          <div class="profile-item">
            <label>Email:</label>
            <span>{{ state.profile.email }}</span>
          </div>
          <div class="profile-item">
            <label>Date de naissance:</label>
            <span>{{ state.profile.dateOfBirth }}</span>
          </div>
          <div class="profile-item">
            <label>Téléphone:</label>
            <span>{{ state.profile.phone }}</span>
          </div>
          <div class="profile-item">
            <label>Adresse:</label>
            <span>{{ state.profile.address }}</span>
          </div>
          <div class="profile-item">
            <label>Pays:</label>
            <span>{{ state.profile.country }}</span>
          </div>
          <div class="profile-item">
            <label>Ville:</label>
            <span>{{ state.profile.city }}</span>
          </div>
          <div class="profile-item">
            <label>Province:</label>
            <span>{{ state.profile.province }}</span>
          </div>
          <div class="profile-item">
            <label>Code postal:</label>
            <span>{{ state.profile.postalCode }}</span>
          </div>
        </div>
      </div>
      <div v-else>
        <p>Chargement...</p>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, inject, reactive, onMounted } from 'vue';
  import { userStore, getUserFromStorage } from "@/components/helpers/userSession";
  import type { ProfileService, UserProfile } from './profil';
  
  export default defineComponent({
    name: 'Profil',
    setup() {
      const profileService = inject('profileService') as ProfileService;
      const state = reactive({
        profile: null as UserProfile | null,
        error: false,
      });
  
      const fetchProfile = async () => {
        try {
          getUserFromStorage();
          const id_user = userStore.user?.session.id_user;

          
          console.log(userStore.user?.session.id_user);
          
         
          if (id_user) {
            const data = await profileService.getUserProfile(id_user);
            state.profile = data;
          } else {
            state.error = true;
          }
        } catch (err) {
          console.error('Erreur lors de la récupération du profil:', err);
          state.error = true;
        }
      };
  
      onMounted(() => {
        fetchProfile();
      });
  
      return {
        state,
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
  
  .profile-card {
    display: flex;
    flex-direction: column;
  }
  
  .profile-item {
    display: flex;
    justify-content: space-between;
    padding: 10px 0;
    border-bottom: 1px solid #ddd;
  }
  
  .profile-item label {
    font-weight: bold;
  }
  
  .profile-item span {
    color: #555;
  }
  </style>