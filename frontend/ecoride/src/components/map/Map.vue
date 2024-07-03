<template>
    <div id="map" ref="mapContainer"></div>
  </template>
  
  <script lang="ts">
  import { defineComponent, onMounted, ref } from 'vue';
  import * as L from 'leaflet';
  
  export default defineComponent({
    name: 'Map',
    setup() {
      const mapContainer = ref<HTMLDivElement | null>(null);
  
      onMounted(() => {
        if (mapContainer.value) {
          // Set the view to Montreal, Canada
          const map = L.map(mapContainer.value).setView([45.5017, -73.5673], 13);
  
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }).addTo(map);
  
          // Add a marker at Montreal's coordinates
          L.marker([45.5017, -73.5673]).addTo(map)
            .bindPopup('Montreal, Canada')
            .openPopup();
        }
      });
  
      return {
        mapContainer,
      };
    },
  });
  </script>
  
  <style scoped>
  #map {
    height: 500px;
    width: 500px;
  }
  </style>
  