<template>
  <div class="home-page">
    <header class="hero-section text-white text-center py-5 mb-4">
      <div class="container">
        <h1 class="display-5 fw-bold">EcoRide</h1>
        <p class="lead mb-0">Location de trottinettes et scooters électriques — simple, rapide, écologique.</p>
      </div>
    </header>

    <section class="container mb-5">
      <div class="card filter-card shadow-sm">
        <div class="card-body">
          <div class="row g-3">
            <div class="col-md-6">
              <label class="form-label fw-semibold">Recherche</label>
              <input v-model="filters.search" class="form-control" placeholder="Modèle ou catégorie" />
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Catégorie</label>
              <select v-model="filters.category" class="form-select">
                <option value="">Toutes</option>
                <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Disponibilité</label>
              <select v-model="filters.availability" class="form-select">
                <option value="">Tous</option>
                <option value="available">Disponible</option>
                <option value="unavailable">Indisponible</option>
              </select>
            </div>
            <div class="col-md-3">
              <label class="form-label fw-semibold">Prix max (CAD/h)</label>
              <input v-model.number="filters.maxPrice" type="number" min="0" class="form-control" />
            </div>
            <div class="col-md-3 d-flex align-items-end">
              <button class="btn btn-outline-secondary w-100" @click="resetFilters">Réinitialiser</button>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="container mb-5">
      <div v-if="state.loading" class="row g-4">
        <div class="col-lg-3 col-md-6 col-sm-6 col-12" v-for="n in 8" :key="n">
          <div class="card h-100 skeleton-card">
            <div class="skeleton-img"></div>
            <div class="card-body">
              <div class="skeleton-line"></div>
              <div class="skeleton-line short"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-else class="row g-4">
        <div class="col-lg-3 col-md-6 col-sm-6 col-12" v-for="scooter in filteredScooters" :key="scooter.id_trotinette">
          <ScooterCard :scooter="scooter" @reserve="openModal(scooter)" />
        </div>
      </div>

      <div v-if="!state.loading && filteredScooters.length === 0" class="text-center text-muted py-5">
        <p class="mb-0">Aucun véhicule ne correspond à vos critères.</p>
      </div>
    </section>

    <ReservationModal :isVisible="state.showModal" v-if="state.showModal" :trotinette="state.selectedTrotinette"
      @close="closeModal" @reserved="handleReservation" />
  </div>
</template>

<script lang="ts">
import { computed, defineComponent, inject, onMounted, reactive } from 'vue';
import ScooterCard from '../scooterCard/ScooterCard.vue';
import { GetTrotinettes, Trotinette } from '../admin/admin';
import ReservationModal from '../reservation/ReservationModal.vue';

export default defineComponent({
  name: 'Home',
  components: { ScooterCard, ReservationModal },
  setup() {
    const trotinettes = inject('getTrotinettes') as GetTrotinettes;
    const state = reactive({ scooters: [] as Trotinette[], loading: false, showModal: false, selectedTrotinette: {} as Trotinette });

    const filters = reactive({ search: '', category: '', availability: '', maxPrice: null as number | null });

    const categories = computed(() => Array.from(new Set(state.scooters.map(s => s.category).filter(Boolean))));

    const filteredScooters = computed(() => {
      let list = state.scooters;
      const q = filters.search.trim().toLowerCase();
      if (q) list = list.filter(s => (s.name + ' ' + (s.category || '')).toLowerCase().includes(q));
      if (filters.category) list = list.filter(s => s.category === filters.category);
      if (filters.availability === 'available') list = list.filter(s => s.available && s.qte > 0);
      else if (filters.availability === 'unavailable') list = list.filter(s => !s.available || s.qte <= 0);
      if (filters.maxPrice != null && Number.isFinite(filters.maxPrice)) list = list.filter(s => s.price <= filters.maxPrice);
      return list;
    });

    const fetchTrotinettes = async () => {
      state.loading = true;
      try {
        state.scooters = await trotinettes.getTrotinettes();
      } finally {
        state.loading = false;
      }
    };

    const resetFilters = () => {
      filters.search = '';
      filters.category = '';
      filters.availability = '';
      filters.maxPrice = null;
    };

    onMounted(fetchTrotinettes);

    const openModal = (scooter: Trotinette) => { state.selectedTrotinette = scooter; state.showModal = true; };
    const closeModal = () => { state.showModal = false; };
    const handleReservation = async () => { await fetchTrotinettes(); };

    return { state, filters, categories, filteredScooters, openModal, closeModal, handleReservation, resetFilters };
  }
});
</script>

<style scoped>
.hero-section {
  background: linear-gradient(135deg, rgba(22,163,74,0.85), rgba(15,118,210,0.75));
  border-radius: 0 0 2rem 2rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
}
.filter-card {
  border: none;
  border-radius: 1rem;
}
.skeleton-card {
  overflow: hidden;
}
.skeleton-img {
  height: 160px;
  background: linear-gradient(90deg, #e9ecef 25%, #f8f9fa 50%, #e9ecef 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
}
.skeleton-line {
  height: 14px;
  margin: 10px 0;
  background: linear-gradient(90deg, #e9ecef 25%, #f8f9fa 50%, #e9ecef 75%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: 999px;
}
.skeleton-line.short { width: 60%; }
@keyframes shimmer {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}
</style>
