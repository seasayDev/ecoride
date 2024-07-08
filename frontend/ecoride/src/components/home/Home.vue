<template>
  <div class="container">
    <div class="row">
      <ScooterCard v-for="(scooter, index) in state.scooters" :key="index" :class="gridClass" :scooter="scooter"
        @reserve="openModal(scooter)">
      </ScooterCard>
    </div>
    <ReservationModal :isVisible="state.showModal" v-if="state.showModal" :trotinette="state.selectedTrotinette"
      @close="closeModal" @reserved="handleReservation" />
  </div>
</template>
  
<script lang="ts">
import { computed, defineComponent, inject, onMounted, reactive } from 'vue';
import ScooterCard from '../scooterCard/ScooterCard.vue';
import { GetTrotinettes, Trotinette } from '../admin';
import ReservationModal from '../reservation/ReservationModal.vue';

export default defineComponent({
  components: {
    ScooterCard,
    ReservationModal,
  },
  setup() {
    const trotinettes = inject('getTrotinettes') as GetTrotinettes;
    const gridClass = computed(() => {
      return { 'col-lg-3 col-md-6 col-sm-6 col-12': true };
    });
    const state = reactive({
      scooters: [] as Array<Trotinette>,
      showModal: false,
      selectedTrotinette: {} as Trotinette,
    });

    onMounted(async () => {
      state.scooters = await trotinettes.getTrotinettes();
    });

    const openModal = (trotinette: Trotinette) => {
      state.selectedTrotinette = trotinette;
      state.showModal = true;
    };

    const closeModal = () => {
      state.showModal = false;
    };

    const handleReservation = async () => {
      // Actualiser la liste des trottinettes après une réservation réussie
      state.scooters = await trotinettes.getTrotinettes();
    };

    return {
      gridClass,
      trotinettes,
      state,
      openModal,
      closeModal,
      handleReservation,
    };
  },
});
</script>
  
<style scoped></style>
  