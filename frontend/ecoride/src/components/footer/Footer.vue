<template>
  <footer class="app-footer py-4 mt-auto">
    <div class="container d-flex flex-wrap justify-content-between align-items-center gap-2">
      <div class="brand">
        <strong>EcoRide</strong> © {{ year }}
      </div>
      <div class="links">
        <router-link to="/aide" class="me-3">Aide</router-link>
        <router-link to="/support">Support</router-link>
      </div>
      <div class="eco">
        <span class="badge bg-success">Écologique</span>
        <span class="badge bg-light text-success ms-1">CO₂ réduit</span>
      </div>
    </div>
  </footer>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'Footer',
  setup() {
    const year = new Date().getFullYear()
    return { year }
  }
})
</script>

<style scoped>
.app-footer {
  background: linear-gradient(180deg,#f8f9fa,#e9ecef);
  font-size: 0.95rem;
  color: #1f2937;
  box-shadow: 0 -4px 30px rgba(0,0,0,0.04);
}
.app-footer .brand { color: #16a34a; }
</style>
