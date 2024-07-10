<template>
  <div class="promotion-container">
    <h1>Gestion des Promotions et Offres Spéciales</h1>
    <button @click="showCreateForm" class="create-button">Créer Nouvelle Offre/Promotion</button>
    <button @click="toggleShowPromotions" class="view-button">
      {{ showPromotions ? 'Masquer les Offres/Promotions' : 'Voir les Offres/Promotions' }}
    </button>
    
    <!-- Formulaire de création/modification -->
    <div v-if="showForm" class="form-container">
      <h2>{{ isEditing ? 'Modifier Offre/Promotion' : 'Créer Nouvelle Offre/Promotion' }}</h2>
      <form @submit.prevent="handleSubmit" class="promotion-form">
        <div class="form-group">
          <label for="description">Description:</label>
          <input type="text" v-model="form.description" required />
        </div>
        <div class="form-group">
          <label for="startDate">Date de début:</label>
          <input type="date" v-model="form.startDate" required />
        </div>
        <div class="form-group">
          <label for="endDate">Date de fin:</label>
          <input type="date" v-model="form.endDate" required />
        </div>
        <div class="form-group">
          <label for="promoCode">Code Promo:</label>
          <input type="text" v-model="form.promoCode" required />
        </div>
        <div class="form-buttons">
          <button type="submit" class="submit-button">{{ isEditing ? 'Modifier' : 'Ajouter' }}</button>
          <button @click="cancelForm" class="cancel-button">Annuler</button>
        </div>
      </form>
    </div>

    <!-- Liste des promotions -->
    <div v-if="promotions.length && showPromotions" class="promotion-list">
      <h2>Offres/Promotions Existantes</h2>
      <ul>
        <li v-for="promotion in promotions" :key="promotion.id" class="promotion-item">
          <div class="promotion-details">
            <p><strong>Description:</strong> {{ promotion.description }}</p>
            <p><strong>Début:</strong> {{ promotion.startDate }}</p>
            <p><strong>Fin:</strong> {{ promotion.endDate }}</p>
            <p><strong>Code Promo:</strong> {{ promotion.promoCode }}</p>
            <div class="promotion-buttons">
              <button @click="editPromotion(promotion)" class="edit-button">Modifier</button>
              <button @click="deletePromotion(promotion.id)" class="delete-button">Supprimer</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      promotions: [],
      showForm: false,
      isEditing: false,
      showPromotions: false,
      form: {
        id: null,
        description: '',
        startDate: '',
        endDate: '',
        promoCode: ''
      }
    };
  },
  created() {
    this.loadPromotions();
  },
  methods: {
    showCreateForm() {
      this.resetForm();
      this.showForm = true;
    },
    toggleShowPromotions() {
      this.showPromotions = !this.showPromotions;
    },
    resetForm() {
      this.form = {
        id: null,
        description: '',
        startDate: '',
        endDate: '',
        promoCode: ''
      };
      this.isEditing = false;
    },
    cancelForm() {
      this.resetForm();
      this.showForm = false;
    },
    handleSubmit() {
      if (this.isEditing) {
        this.updatePromotion();
      } else {
        this.addPromotion();
      }
    },
    addPromotion() {
      const newPromotion = { ...this.form, id: Date.now() };
      this.promotions.push(newPromotion);
      this.savePromotions();
      this.resetForm();
      this.showForm = false;
    },
    editPromotion(promotion) {
      this.form = { ...promotion };
      this.isEditing = true;
      this.showForm = true;
    },
    updatePromotion() {
      const index = this.promotions.findIndex(p => p.id === this.form.id);
      if (index !== -1) {
        this.promotions.splice(index, 1, this.form);
      }
      this.savePromotions();
      this.resetForm();
      this.showForm = false;
    },
    deletePromotion(id) {
      if (confirm("Êtes-vous sûr de vouloir supprimer cette promotion ?")) {
        this.promotions = this.promotions.filter(p => p.id !== id);
        this.savePromotions();
      }
    },
    savePromotions() {
      localStorage.setItem('promotions', JSON.stringify(this.promotions));
    },
    loadPromotions() {
      const promotions = localStorage.getItem('promotions');
      if (promotions) {
        this.promotions = JSON.parse(promotions);
      }
    }
  }
};
</script>

<style>
.promotion-container {
  text-align: center;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  font-family: Arial, sans-serif;
}

h1 {
  color: #333;
}

.create-button, .submit-button, .cancel-button, .edit-button, .delete-button, .view-button {
  padding: 10px 20px;
  margin: 5px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.create-button {
  background-color: #28a745;
  color: white;
}

.view-button {
  background-color: #17a2b8;
  color: white;
}

.submit-button {
  background-color: #007bff;
  color: white;
}

.cancel-button {
  background-color: #dc3545;
  color: white;
}

.edit-button {
  background-color: #ffc107;
  color: black;
}

.delete-button {
  background-color: #dc3545;
  color: white;
}

.form-container, .promotion-list {
  margin-top: 20px;
}

.promotion-form .form-group {
  margin-bottom: 15px;
}

.promotion-form .form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.promotion-form .form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.promotion-form .form-buttons {
  display: flex;
  justify-content: center;
}

.promotion-list ul {
  list-style: none;
  padding: 0;
}

.promotion-item {
  background-color: #f8f9fa;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.promotion-details p {
  margin: 5px 0;
}

.promotion-buttons {
  margin-top: 10px;
}
</style>
