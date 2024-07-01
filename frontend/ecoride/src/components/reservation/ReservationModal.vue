<template>
    <div class="modal" v-if="isVisible">
      <div class="modal-content">
        <span class="close" @click="closeModal">&times;</span>
        <h2>Réserver une trottinette</h2>
        <p>Trottinettes disponibles : {{ trotinette.qte }}</p>
        <form @submit.prevent="submitReservation">
          <label for="date">Date de réservation:</label>
          <input type="date" v-model="reservationDate" required>
          <label for="time">Durée de réservation (heures):</label>
          <input type="number" v-model="reservationDuration" required>
          <button type="submit">Suivant</button>
        </form>
        <div v-if="showConfirmation">
          <p>Coût total: {{ totalCost }}</p>
          <p>Confirmez-vous la réservation ?</p>
          <button @click="confirmReservation">Oui</button>
          <button @click="closeModal">Non</button>
        </div>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, PropType, ref } from 'vue';
  import axios from 'axios';
  import { Trotinette } from '../scooterCard';
  
  export default defineComponent({
    props: {
      isVisible: {
        type: Boolean as PropType<boolean>,
        required: true,
      },
      trotinette: {
        type: Object as PropType<Trotinette>,
        required: true,
      },
    },
    emits: ['close', 'reserved'],
    setup(props, { emit }) {
      const reservationDate = ref('');
      const reservationDuration = ref(1);
      const showConfirmation = ref(false);
      const totalCost = ref(0);
  
      const closeModal = () => {
        emit('close');
      };
  
      const submitReservation = () => {
        totalCost.value = props.trotinette.price * reservationDuration.value;
        showConfirmation.value = true;
      };
  
      const confirmReservation = async () => {
        try {
          const response = await axios.post('http://127.0.0.1:5000/reserve', {
            trotinette_id: props.trotinette.id_trotinette,
            user_id: 1, // Remplacez par l'ID utilisateur approprié
            start_date: reservationDate.value,
            duration: reservationDuration.value,
            total_cost: totalCost.value,
          });
          console.log(response.data);
          emit('reserved');
          closeModal();
        } catch (error) {
          console.error('Erreur lors de la réservation:', error);
        }
      };
  
      return {
        reservationDate,
        reservationDuration,
        showConfirmation,
        totalCost,
        closeModal,
        submitReservation,
        confirmReservation,
      };
    },
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
    overflow: auto;
    background-color: rgba(0, 0, 0, 0.4);
  }
  
  .modal-content {
    background-color: #fefefe;
    padding: 20px;
    border: 1px solid #888;
    width: 80%;
    max-width: 600px;
    position: relative;
  }
  
  .close {
    position: absolute;
    top: 10px;
    right: 10px;
    color: #aaa;
    font-size: 28px;
    font-weight: bold;
    cursor: pointer;
  }
  
  .close:hover,
  .close:focus {
    color: black;
    text-decoration: none;
    cursor: pointer;
  }
  </style>
  