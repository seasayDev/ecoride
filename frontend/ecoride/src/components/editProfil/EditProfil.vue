<template>
    <div class="container mt-5">
      <h2>Modifier le Profil</h2>
      <form @submit.prevent="updateProfile">
        <div class="form-grid">
          <div class="form-group">
            <label for="firstName">Prénom</label>
            <input type="text" class="form-control" id="firstName" v-model="profile.firstName" required>
          </div>
          <div class="form-group">
            <label for="lastName">Nom</label>
            <input type="text" class="form-control" id="lastName" v-model="profile.lastName" required>
          </div>
          <div class="form-group">
            <label for="email">Email</label>
            <input type="email" class="form-control" id="email" v-model="profile.email" required>
          </div>
          <div class="form-group">
            <label for="dateOfBirth">Date de naissance</label>
            <input type="date" class="form-control" id="dateOfBirth" v-model="profile.dateOfBirth" required>
          </div>
          <div class="form-group">
            <label for="phone">Téléphone</label>
            <input type="text" class="form-control" id="phone" v-model="profile.phone" required>
          </div>
          <div class="form-group">
            <label for="address">Adresse</label>
            <input type="text" class="form-control" id="address" v-model="profile.address" required>
          </div>
          <div class="form-group">
            <label for="country">Pays</label>
            <input type="text" class="form-control" id="country" v-model="profile.country" required>
          </div>
          <div class="form-group">
            <label for="city">Ville</label>
            <input type="text" class="form-control" id="city" v-model="profile.city" required>
          </div>
          <div class="form-group">
            <label for="province">Province</label>
            <input type="text" class="form-control" id="province" v-model="profile.province" required>
          </div>
          <div class="form-group">
            <label for="postalCode">Code postal</label>
            <input type="text" class="form-control" id="postalCode" v-model="profile.postalCode" required>
          </div>
        </div>
        <button type="submit" class="btn btn-primary mt-4">Enregistrer</button>
      </form>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, reactive, onMounted } from 'vue';
  import { useRoute, useRouter } from 'vue-router';
  import { userStore, getUserFromStorage } from "@/components/helpers/userSession";
  import { EditProfileService } from './editprofil';
  
  export default defineComponent({
    name: 'EditProfil',
    setup() {
      const route = useRoute();
      const router = useRouter();
      const editProfileService = new EditProfileService('http://localhost:5000');
      const profile = reactive({
        firstName: '',
        lastName: '',
        email: '',
        dateOfBirth: '',
        phone: '',
        address: '',
        country: '',
        city: '',
        province: '',
        postalCode: ''
      });
  
      const fetchProfile = async () => {
        try {
          getUserFromStorage();
          const id_user = userStore.user?.session.id_user;
          if (id_user) {
            const data = await editProfileService.getUserProfile(id_user);
            Object.assign(profile, data);
          } else {
            console.error('ID utilisateur non trouvé');
          }
        } catch (error) {
          console.error('Erreur lors de la récupération du profil:', error);
        }
      };
  
      const updateProfile = async () => {
        try {
          const id_user = userStore.user?.session.id_user;
          if (id_user) {
            await editProfileService.updateUserProfile(id_user, profile);
            router.push({ name: 'Profil' });
          } else {
            console.error('ID utilisateur non trouvé');
          }
        } catch (error) {
          console.error('Erreur lors de la mise à jour du profil:', error);
        }
      };
  
      onMounted(() => {
        fetchProfile();
      });
  
      return {
        profile,
        updateProfile
      };
    },
  });
  </script>
  
  <style scoped>
  .container {
    background-color: var(--blue-light);
    padding: 20px;
    border-radius: 8px;
    color: #fff;
    max-width: 800px;
    margin: auto;
  }
  
  .form-grid {
    display: grid;
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .form-group {
    display: flex;
    flex-direction: column;
  }
  
  .form-control {
    font-size: 1em;
    padding: 10px;
    border-radius: 4px;
    border: 1px solid #ccc;
  }
  
  .btn {
    font-size: 1.2em;
    padding: 10px 20px;
    background-color: #007bff;
    color: #fff;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .btn:hover {
    background-color: #0056b3;
  }
  
  @media (min-width: 768px) {
    .form-grid {
      grid-template-columns: 1fr 1fr;
    }
  }
  </style>