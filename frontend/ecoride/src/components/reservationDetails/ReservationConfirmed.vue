<template>
    <div class="container text-center mt-5">
        <div class="card mx-auto shadow-sm" style="max-width: 500px;">
            <div class="card-body">
                <h1 class="card-title text-success">Reservation Confirmed</h1>
                <p class="card-text">Thank you for your reservation! Here are your reservation details:</p>
                <ul class="list-group list-group-flush text-left">
                    <li class="list-group-item"><strong>Nom:</strong> {{ trotinette.name }}</li>
                    <li class="list-group-item"><strong>Date de réservation:</strong> {{ reservationDate }}</li>
                    <li class="list-group-item"><strong>Heure de début:</strong> {{ reservationTime }}</li>
                    <li class="list-group-item"><strong>Durée de réservation (heures):</strong> {{ reservationDuration }}
                    </li>
                    <li class="list-group-item"><strong>Lieu de départ:</strong> {{ trotinette.location.name }}</li>
                    <li class="list-group-item"><strong>Lieu de retour:</strong> {{ dropOutName }}</li>
                    <li class="list-group-item"><strong>Coût total:</strong> {{ totalCost }}</li>
                </ul>
                <a href="/" class="btn btn-primary mt-3">Retour à l'accueil</a>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useRoute } from 'vue-router';

export default defineComponent({
    setup() {
        const route = useRoute();
        const { trotinette, reservationDate, reservationTime, reservationDuration, dropOutLocation, totalCost, dropOutName } = route.query;

        return {
            trotinette: JSON.parse(trotinette as string),
            reservationDate,
            reservationTime,
            reservationDuration,
            dropOutLocation,
            totalCost,
            dropOutName
        };
    }
});
</script>

<style scoped>
.card {
    border: 1px solid #007bff;
    box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.1), 0 6px 20px 0 rgba(0, 0, 0, 0.1);
}

.card-title {
    color: #28a745;
    /* Success color */
}

.card-body {
    padding: 20px;
}

.list-group-item {
    text-align: left;
}

.container {
    background-color: #f8f9fa;
    /* Light gray background */
    padding: 20px;
    border-radius: 10px;
}
</style>
