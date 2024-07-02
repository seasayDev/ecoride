<template>
  <div class="container">
    <div class="alert" v-if="state.error">
      Erreur lors de la récupération du profil utilisateur!
    </div>
    <div v-if="state.profile">
      <h2>Profil Utilisateur</h2>
      <div class="profile-card">
        <div class="profile-picture">
          <font-awesome-icon icon="user" size="6x" />
        </div>
        <div class="profile-details">
          <div class="profile-item">
            <font-awesome-icon icon="user" class="profile-icon" />
            <label>Prénom:</label>
            <span>{{ state.profile.firstName }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="user" class="profile-icon" />
            <label>Nom:</label>
            <span>{{ state.profile.lastName }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="envelope" class="profile-icon" />
            <label>Email:</label>
            <span>{{ state.profile.email }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="calendar-alt" class="profile-icon" />
            <label>Date de naissance:</label>
            <span>{{ state.profile.dateOfBirth }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="phone" class="profile-icon" />
            <label>Téléphone:</label>
            <span>{{ state.profile.phone }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="map-marker-alt" class="profile-icon" />
            <label>Adresse:</label>
            <span>{{ state.profile.address }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="globe" class="profile-icon" />
            <label>Pays:</label>
            <span>{{ state.profile.country }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="city" class="profile-icon" />
            <label>Ville:</label>
            <span>{{ state.profile.city }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="map" class="profile-icon" />
            <label>Province:</label>
            <span>{{ state.profile.province }}</span>
          </div>
          <div class="profile-item">
            <font-awesome-icon icon="mail-bulk" class="profile-icon" />
            <label>Code postal:</label>
            <span>{{ state.profile.postalCode }}</span>
          </div>
        </div>
        <div class="btn-container">
          <button class="btn" @click="editProfile">Modifier le profil</button>
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
import { useRouter } from 'vue-router';
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
    const router = useRouter();

    const fetchProfile = async () => {
      try {
        getUserFromStorage();
        const id_user = userStore.user?.session.id_user;

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

    const editProfile = () => {
      router.push({ name: 'EditProfil' });
    };

    onMounted(() => {
      fetchProfile();
    });

    return {
      state,
      editProfile,
    };
  },
});
</script>

<style scoped>
html, body {
  height: 100%;
  margin: 0;
}

h2 {
  text-align: center;
  padding-bottom: 4%;
}

.container {
  background-color: var(--blue-light);
  padding: 20px;
  border-radius: 8px;
  color: #fff;
  max-width: 1200px;
  margin: 50px auto; 
  min-height: calc(100vh - 100px); 
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.alert {
  background-color: #f8d7da;
  color: #721c24;
  padding: 10px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.profile-picture {
  margin-bottom: 20px;
}

.profile-details {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  width: 100%;
}

.profile-item {
  display: flex;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ddd;
}

.profile-item label {
  font-weight: bold;
  margin-left: 10px;
  margin-right: 5px;
  font-size: 1.2em;
}

.profile-item span {
  color: #ddd;
  font-size: 1.2em;
}

.profile-icon {
  font-size: 1.5em;
  margin-right: 10px;
}

.btn-container {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%; 
  margin-top: 20px;
}

.btn {
  width: 200px; 
  height: 50px; 
  font-size: 1.2em; 
  background-color: #007bff;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: #0056b3;
}

@media (max-width: 768px) {
  .profile-details {
    grid-template-columns: 1fr;
  }

  .profile-item {
    flex-direction: column;
    align-items: flex-start;
  }

  .profile-item label, .profile-item span {
    font-size: 1em;
  }

  .profile-icon {
    font-size: 1.5em;
    padding-bottom: 10%;
  }
}
</style>