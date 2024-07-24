<template>
    <div class="container mt-4">
        <h2>Reservation History</h2>
        <div v-if="loading" class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <div v-if="successMessage" class="alert alert-success" role="alert">
            {{ successMessage }}
        </div>
        <div v-if="reservations.length > 0" class="list-group">
            <div v-for="reservation in reservations" :key="reservation.id_reservation">
                <div class="list-group-item mb-3 reservation-card">
                    <div class="reservation-summary">
                        <p class="mb-2"><strong>Start Date:</strong> {{ reservation.start_date }}</p>
                        <p class="mb-2"><strong>End Date:</strong> {{ reservation.end_date }}</p>
                        <p class="mb-2"><strong>Pick-up Location:</strong> {{ reservation.pick_up_location.name }}</p>
                        <p class="mb-2"><strong>Drop-off Location:</strong> {{ reservation.drop_off_location.name }}</p>
                        <p class="mb-2"><strong>Total Cost:</strong> ${{ reservation.total_cost }}</p>
                        <img v-if="reservation.trotinette.image.data" :src="getImageSrc(reservation.trotinette.image.data)"
                            alt="Trotinette Image" class="img-thumbnail mb-3 trotinette-image" />
                    </div>
                    <div class="reservation-advanced">
                        <h6 class="mb-2"><strong>Trotinette Details:</strong></h6>
                        <p class="mb-2"><strong>Model:</strong> {{ reservation.trotinette.model }}</p>
                        <p class="mb-2"><strong>Category:</strong> {{ reservation.trotinette.category }}</p>
                        <p class="mb-2"><strong>Price:</strong> ${{ reservation.trotinette.price }}</p>
                        <h6 class="mb-2"><strong>User Details:</strong></h6>
                        <p class="mb-2"><strong>Name:</strong> {{ reservation.user.first_name }} {{ reservation.user.last_name
                        }}</p>
                    </div>
                </div>
                <button class="btn btn-primary mt-3" @click="deverrouiller(reservation.id_reservation)">Deverrouiller</button>
            </div>
            
            
        </div>
        
        <div v-else class="alert alert-info" role="alert">
            No reservations found.
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, inject } from 'vue';
import axios from 'axios';
import { Reservation, ReservationsService } from './reservationsService';
import { userStore, setUser, getUserFromStorage } from "@/components/helpers/userSession";
import { Reservation, ReservationsService } from '@/components/reservationHistory/reservationsService';



export default defineComponent({
    name: 'ReservationHistory',
    setup() {
        const reservations = ref<Reservation[]>([]);
        const loading = ref<boolean>(true);
        const error = ref<string | null>(null);
        const successMessage = ref<string | null>(null);

        const reservationsService = inject<ReservationsService>('ReservationsHistoryService');
        if (!reservationsService) {
            throw new Error('ReservationsHistoryService not provided');
        }

        const fetchReservations = async (userId: number) => {
            try {
                reservations.value = await reservationsService.getReservations(userId);
                console.log(reservations.value);
            } catch (err) {
                error.value = 'Failed to fetch reservations';
            } finally {
                loading.value = false;
            }
        };

        const cancelReservation = async (reservationId: number) => {
        try {
        await reservationsService.cancelReservation(reservationId);
        // Mettre à jour la liste des réservations localement
        reservations.value = reservations.value.filter(reservation => reservation.id_reservation !== reservationId);
        } catch (err) {
        error.value = 'Failed to cancel reservation';
        }
        };

        const getImageSrc = (imageData: string) => {
            return `data:image/webp;base64,${imageData}`;
        };

        const deverrouiller = async (id_reservation: number) => {
            try {
                const response = await axios.post('http://localhost:5000/unlockTrotinette', { id_reservation });
                if (response.status === 200) {
                    successMessage.value = response.data.message;
                    // Remove the reservation from the list
                    reservations.value = reservations.value.filter(reservation => reservation.id_reservation !== id_reservation);
                } else {
                    throw new Error('Failed to unlock trotinette');
                }
            } catch (error) {
                error.value = 'Failed to unlock trotinette';
            }
        };

        onMounted(() => {
            getUserFromStorage();
            const userId = userStore.user?.session.id_user;
            fetchReservations(userId);
        });

        return {
            reservations,
            loading,
            error,
            successMessage,
            getImageSrc,
            deverrouiller,
        };
    },
});
</script>

<style scoped>
.container {
    margin-top: 20px;
}

.spinner-border {
    display: block;
    margin: 0 auto;
}

.img-thumbnail {
    max-width: 100%;
    height: auto;
    display: block;
    margin-top: 10px;
}

.trotinette-image {
    width: 40px;
    height: 40px;
    object-fit: cover;
}

.reservation-card {
    position: relative;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease-in-out;
}

.reservation-card:hover {
    transform: scale(1.02);
    box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.reservation-advanced {
    display: none;
}

.reservation-card:hover .reservation-advanced {
    display: block;
    position: absolute;
    top: 0;
    left: 0;
    background: white;
    width: 100%;
    height: 100%;
    padding: 10px;
    z-index: 10;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>

<style scoped>
.container {
  margin-top: 20px;
}

.spinner-border {
  display: block;
  margin: 0 auto;
}

.img-thumbnail {
  max-width: 100%;
  height: auto;
  display: block;
  margin-top: 10px;
}

.trotinette-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
}

.reservation-card {
  position: relative;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease-in-out;
  padding-top: 40px; /* espace pour le bouton d'annulation */
}

.reservation-card:hover {
  transform: scale(1.02);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.reservation-advanced {
  display: none;
}

.reservation-card:hover .reservation-advanced {
  display: block;
  position: absolute;
  top: 0;
  left: 0;
  background: white;
  width: 100%;
  height: 100%;
  padding: 10px;
  z-index: 10;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.cancel-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  border-radius: 5px;
  z-index: 20; /* pour être sûr que le bouton est au-dessus de tout */
}

.cancel-button:hover {
  background-color: #ff1a1a;
}
</style>

