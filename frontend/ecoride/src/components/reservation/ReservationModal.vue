<template>
  <div class="modal" id="reservationModal" tabindex="-1" role="dialog" aria-labelledby="reservationModalLabel"
    aria-hidden="true" v-if="isVisible">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="reservationModalLabel">{{ trotinette.name }}</h5>
          <button type="button" class="btn-close" @click="closeModal" aria-label="Close"></button>
        </div>
        <div class="modal-body">
          <p>Trottinettes disponibles : {{ trotinette.qte }}</p>
          <form v-if="currentStep === 'form'" @submit.prevent="showConfirmationStep">
            <div class="row">
              <div class="col-md-6 form-group">
                <label for="date">Date de réservation :</label>
                <input type="date" class="form-control" v-model="reservationDate" :min="today" required>
              </div>
              <div class="col-md-6 form-group">
                <label for="time">Heure de début :</label>
                <input type="time" class="form-control" v-model="state.reservationTime" :min="minTime" :max="maxTime"
                  @change="validateTime" required>
              </div>
              <div class="col-md-6 form-group">
                <label for="duration">Durée de réservation (heures) :</label>
                <input type="number" class="form-control" v-model="reservationDuration" min="1" max="8" required>
              </div>
            </div>
            <div class="row">
              <div class="col-md-6 form-group">
                <label for="pickup-location">Lieu de départ :</label>
                <input type="text" class="form-control" :placeholder="trotinette.location.name" required disabled>
              </div>
              <div class="col-md-6 form-group">
                <label for="location" class="form-label">Lieu de retour :</label>
                <select class="form-control" id="location" v-model="state.dropOutLocation" required>
                  <option v-for="location in state.locations" :key="location.id" :value="location.name">
                    {{ location.name }}
                  </option>
                </select>
              </div>
            </div>
            <div class="row mt-3">
              <div class="col-12">
                <div class="p-2 bg-light">
                  <p>Coût total : {{ costToshow }}</p>
                </div>
              </div>
            </div>
            <button type="submit" class="btn btn-primary mt-3">Suivant</button>
          </form>

          <div v-if="currentStep === 'confirmation'" class="confirmation">
            <h5>Confirmation de la réservation</h5>
            <p><strong>Date de réservation :</strong> <span>{{ reservationDate }}</span></p>
            <p><strong>Heure de début :</strong> <span>{{ state.reservationTime }}</span></p>
            <p><strong>Durée de réservation (heures) :</strong> <span>{{ reservationDuration }}</span></p>
            <p><strong>Lieu de départ :</strong> <span>{{ trotinette.location.name }}</span></p>
            <p><strong>Lieu de retour :</strong> <span>{{ state.dropOutLocation }}</span></p>
            <p><strong>Coût total :</strong> <span>{{ costToshow }}</span></p>
            <div class="d-flex justify-content-between mt-3">
              <button class="btn btn-secondary w-50 me-2" @click="editReservation">Éditer</button>
              <button class="btn btn-success w-50 ms-2" @click="confirmReservation">Confirmer</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, PropType, ref, watch, inject, onMounted, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { Trotinette } from '../scooterCard';
import { userStore, getUserFromStorage } from "@/components/helpers/userSession";
import { Location, Newscooter, GetTrotinettes } from '../admin';

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
    const trotinettesLocations = inject('getTrotinettes') as GetTrotinettes;
    const reservationDate = ref('');
    const reservationDuration = ref(1);
    const showConfirmation = ref(false);
    const totalCost = ref(0);
    const minTime = ref('08:00');
    const maxTime = ref('20:00');
    const currentStep = ref('form');
    const router = useRouter();
    const state = reactive({
      locations: [] as Array<Location>,
      dropOutLocation: '' as string,
      reservationTime: '08:00',
    });

    const closeModal = () => {
      emit('close');
    };

    onMounted(async () => {
      state.locations = await trotinettesLocations.getLocations();
    });

    watch(() => props.trotinette, (newValue) => {
      // console.log(newValue);
    });

    const costToshow = computed(() => props.trotinette.price * reservationDuration.value);

    getUserFromStorage();

    const showConfirmationStep = () => {
      currentStep.value = 'confirmation';
    };

    const editReservation = () => {
      currentStep.value = 'form';
    };

    const confirmReservation = () => {
      const reservationDetails = {
        trotinette: props.trotinette,
        user_id: userStore.user?.session.id_user,
        reservationDate: reservationDate.value,
        reservationTime: state.reservationTime,
        reservationDuration: reservationDuration.value,
        dropOutLocation: state.dropOutLocation,
        totalCost: costToshow.value,
      };

      localStorage.setItem('reservationDetails', JSON.stringify(reservationDetails));
      router.push({ name: 'ReservationDetails' });
    };

    const today = computed(() => {
      const date = new Date();
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, '0');
      const day = String(date.getDate()).padStart(2, '0');
      return `${year}-${month}-${day}`;
    });

    const validateTime = () => {
      const time = state.reservationTime;
      if (time < minTime.value) {
        state.reservationTime = minTime.value;
      } else if (time > maxTime.value) {
        state.reservationTime = maxTime.value;
      }
    };

    return {
      reservationDate,
      reservationDuration,
      showConfirmation,
      totalCost,
      closeModal,
      showConfirmationStep,
      editReservation,
      confirmReservation,
      costToshow,
      trotinettesLocations,
      state,
      today,
      minTime,
      maxTime,
      currentStep,
      validateTime,
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
  min-width: 700px;
  position: relative;
}

.confirmation p {
  background-color: #f8f9fa;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.confirmation p span {
  margin-left: auto;
}

.d-flex {
  display: flex !important;
}

.justify-content-between {
  justify-content: space-between !important;
}

.mt-3 {
  margin-top: 1rem !important;
}

.me-2 {
  margin-right: 0.5rem !important;
}

.ms-2 {
  margin-left: 0.5rem !important;
}

.w-50 {
  width: 50% !important;
}

/* Add this CSS to ensure consistent width for input and select elements */
.form-control,
.form-select {
  width: 100%;
}
</style>
