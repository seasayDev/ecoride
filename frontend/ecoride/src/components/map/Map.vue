<template>
  <div class="container-fluid vh-100 d-flex flex-column">
    <div class="row flex-grow-1">
      <div id="map" ref="mapContainer" class="col-12"></div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, onMounted, ref, createApp, h } from 'vue';
import * as L from 'leaflet';
import PopupContent from './PopupContent.vue';

// Import the scooter image
import scooterImage from '../../images/map_scooter.png';

export default defineComponent({
  name: 'Map',
  setup() {
    const mapContainer = ref<HTMLDivElement | null>(null);
    const pk_pavillon =[[45.50837995371091, -73.5687737935345]]
    // Coordinates to follow
    const pathCoordinates = [
      [45.50837995371091, -73.5687737935345],
      [45.509041520402015, -73.56825879218617],
      [45.50949257619858, -73.5677438015266],
      [45.50976321578439, -73.56755066627115],
      [45.51018421118423, -73.56727168605927],
      [45.51068039210224, -73.56707851810063],
      [45.5112968583698, -73.56684241744615],
      [45.511823105148636, -73.56658486600429],
      [45.51159753479096, -73.56619867204613],
      [45.51143210234184, -73.56574810095681],
      [45.511131316677606, -73.56499715705671],
      [45.51125159309636, -73.56484693967992],
      [45.511447046337786, -73.56465379522892],
      [45.511792843331094, -73.56426750956649],
      [45.51260473561558, -73.56362364390046],
      [45.51343164329551, -73.5628080904959],
      [45.51403304089576, -73.56233588864237],
      [45.514604362541085, -73.56184222283024],
      [45.51514560827491, -73.56132709297984],
      [45.51535814459017, -73.5610757472835],
      [45.51550104863681, -73.561386899875],
      [45.51567092543739, -73.56170586418152],
      [45.516471125370884, -73.56346019927666],
      [45.51698073643786, -73.5645192008778],
      [45.517075950715025, -73.5647545949472],
      [45.51701560422602, -73.56479606192643],
      [45.517179729815936, -73.56515020709925],
      [45.517424259154126, -73.56572678104202],
      [45.51769801426867, -73.56634886504449],
      [45.51812326981531, -73.56729717075802],
      [45.5186867278947, -73.56858307083849],
      [45.518963145046456, -73.5691937780755],
      [45.518998515483915, -73.56925642460351],
      [45.51908120705007, -73.56917193458138],
      [45.51913852732625, -73.569118289963],
      [45.51923117421313, -73.56911107693377],
      [45.51943903317767, -73.56890574039144],
      [45.5197298126101, -73.56860350532095],
      [45.519958958467804, -73.56842081697636],
      [45.52027343941683, -73.56811858273335],
      [45.52044569263199, -73.56796069758204],
    ];

    // Coordinates for Montreal
    const montrealCoordinates = [45.5017, -73.5673];

    onMounted(() => {
      if (mapContainer.value) {
        const map = L.map(mapContainer.value).setView(montrealCoordinates, 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        }).addTo(map);

        // Add a green transparent circle centered on Montreal
        L.circle(montrealCoordinates, {
          color: 'green',
          fillColor: 'green',
          fillOpacity: 0.1,
          radius: 5000
        }).addTo(map);

        // Custom icon for the electric scooter
        const scooterIcon = L.icon({
          iconUrl: scooterImage,
          iconSize: [38, 38], // Adjust the size as needed
          iconAnchor: [19, 19], // Anchor the icon at the center
        });

        const marker = L.marker(pathCoordinates[0], { icon: scooterIcon }).addTo(map)
          .bindPopup('Moving Scooter')
          .openPopup();

        const pathLine = L.polyline([pathCoordinates[0]], { color: 'blue' }).addTo(map);

        let step = 0;

        const interval = setInterval(() => {
          step += 1;
          if (step >= pathCoordinates.length) {
            clearInterval(interval);
            marker.bindPopup('Arrived').openPopup();
            return;
          }

          marker.setLatLng(pathCoordinates[step]);
          pathLine.addLatLng(pathCoordinates[step]);
        }, 1000); // Update every second

        const blueDotIcon = L.divIcon({
          html: '<i class="bi bi-shop" style="color: blue; font-size: 24px;"></i>',
          className: 'custom-blue-dot-icon',
          iconSize: [24, 24],
          iconAnchor: [12, 12], // Adjust as needed
        });
        const blueDotMarker = L.marker(pk_pavillon[0], { icon: blueDotIcon }).addTo(map);

        blueDotMarker.on('click', () => {
          const popupContent = document.createElement('div');
          const popupApp = createApp({
            render: () => h(PopupContent)
          });
          popupApp.mount(popupContent);
          blueDotMarker.bindPopup(popupContent).openPopup();
        });
      
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
