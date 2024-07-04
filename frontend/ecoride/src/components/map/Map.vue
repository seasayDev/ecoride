<template>
  <div class="container-fluid vh-100 d-flex flex-column">
    <div class="row flex-grow-1">
      <div id="map" ref="mapContainer" class="col-12"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref } from 'vue';
import * as L from 'leaflet';

// Import the scooter image
import scooterImage from '../../images/map_scooter.png';

export default defineComponent({
  name: 'Map',
  setup() {
    const mapContainer = ref<HTMLDivElement | null>(null);

    const uqamCoordinates = [45.508888, -73.561668];
    const concordiaCoordinates = [45.497268, -73.579065];

    onMounted(() => {
      if (mapContainer.value) {
        const map = L.map(mapContainer.value).setView(uqamCoordinates, 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Custom icon for the electric scooter
        const scooterIcon = L.icon({
          iconUrl: scooterImage,
          iconSize: [38, 38], // Adjust the size as needed
          iconAnchor: [19, 19], // Anchor the icon at the center
        });

        const marker = L.marker(uqamCoordinates, { icon: scooterIcon }).addTo(map)
          .bindPopup('Moving Scooter')
          .openPopup();

        const pathLine = L.polyline([uqamCoordinates], { color: 'blue' }).addTo(map);

        let currentLat = uqamCoordinates[0];
        let currentLng = uqamCoordinates[1];
        const totalSteps = 100; // Number of steps to reach Concordia
        let step = 0;

        const interval = setInterval(() => {
          step += 1;
          currentLat += (concordiaCoordinates[0] - uqamCoordinates[0]) / totalSteps;
          currentLng += (concordiaCoordinates[1] - uqamCoordinates[1]) / totalSteps;

          marker.setLatLng([currentLat, currentLng]);
          pathLine.addLatLng([currentLat, currentLng]);

          if (step >= totalSteps) {
            clearInterval(interval);
            marker.bindPopup('Arrived at Concordia University').openPopup();
          }
        }, 1000); // Update every 100 milliseconds
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
  height: 100%;
}
</style>
