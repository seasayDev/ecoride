<template>
    <div class="container mt-4">
        <h2>Reservation History</h2>
        <div v-if="loading" class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
        <div v-if="error" class="alert alert-danger" role="alert">
            {{ error }}
        </div>
        <div v-if="reservations.length > 0" class="list-group">
            <div v-for="reservation in reservations" :key="reservation.id_reservation"
                class="reservation-container">
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
                </div>
                <button @click="pay(reservation)" class="btn btn-primary mt-3">Pay</button>
            </div>
        </div>
        <div v-else class="alert alert-info" role="alert">
            No reservations found.
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted, inject } from 'vue';
import { useRouter } from 'vue-router';
import { Reservation, ReservationsService } from './reservationsService';
import { userStore, getUserFromStorage } from "@/components/helpers/userSession";

export default defineComponent({
    name: 'ReservationHistory',
    setup() {
        const reservations = ref<Reservation[]>([]);
        const loading = ref<boolean>(true);
        const error = ref<string | null>(null);
        const router = useRouter();

        const reservationsService = inject<ReservationsService>('ReservationsHistoryService');
        if (!reservationsService) {
            throw new Error('ReservationsHistoryService not provided');
        }

        const fetchReservations = async (userId: number) => {
            try {
                reservations.value = await reservationsService.getReservations(userId);
                console.log(reservations.value)
            } catch (err) {
                error.value = 'Failed to fetch reservations';
            } finally {
                loading.value = false;
            }
        };

        const getImageSrc = (imageData: string) => {
            return `data:image/webp;base64,${imageData}`;
        };

        const pay = (reservation: Reservation) => {
            router.push({
                name: 'ReservationDetails',
                query: {
                    reservationId: reservation.id_reservation,
                    trotinette: JSON.stringify(reservation.trotinette),
                    reservationDate: reservation.start_date,
                    reservationTime: reservation.start_date,
                    reservationDuration: (new Date(reservation.end_date).getTime() - new Date(reservation.start_date).getTime()) / (1000 * 60 * 60),
                    dropOutLocation: reservation.drop_off_location.name,
                    totalCost: reservation.total_cost
                }
            });
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
            getImageSrc,
            pay
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

.reservation-container {
    margin-bottom: 20px;
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

.btn-primary {
    margin-top: 10px;
}
</style>
