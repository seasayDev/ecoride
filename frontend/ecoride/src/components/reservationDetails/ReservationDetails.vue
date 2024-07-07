<template>
    <div class="container-fluid">
        <div class="row">
            <!-- Reservation Details Section -->
            <div class="col-md-8 reservation-details" v-if="trotinette">
                <h1>Détails de la Réservation</h1>
                <img v-if="trotinette.image && trotinette.image.data"
                    :src="'data:image/png;base64,' + trotinette.image.data" alt="Trotinette Image"
                    class="trotinette-image" />
                <p><strong>Nom:</strong> {{ trotinette.name }}</p>
                <p><strong>Date de réservation:</strong> {{ reservationDate }}</p>
                <p><strong>Heure de début:</strong> {{ reservationTime }}</p>
                <p><strong>Durée de réservation (heures):</strong> {{ reservationDuration }}</p>
                <p><strong>Lieu de départ:</strong> {{ trotinette.location.name }}</p>
                <p><strong>Lieu de retour:</strong> {{ dropOutLocation }}</p>
                <p><strong>Coût total:</strong> {{ totalCost }}</p>
            </div>

            <!-- Loading State -->
            <div v-else>
                <p>Chargement des détails de la réservation...</p>
            </div>

            <!-- Payment Form Section -->
            <div class="col-md-4 payment-form d-flex align-items-center">
                <div class="w-100">
                    <p class="text-muted">
                        <i class="bi bi-info-circle-fill"></i> Un dépôt de 200 $ sera prélevé sur votre carte de crédit et
                        vous sera restitué une fois la trottinette retournée au lieu de retour.
                    </p>
                    <h2>Détails de paiement</h2>
                    <div class="card-selection row">
                        <div class="col-6" :class="{ selected: selectedCard === 'visa' }" @click="selectCardType('visa')">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/4/41/Visa_Logo.png" alt="Visa">
                        </div>
                        <div class="col-6" :class="{ selected: selectedCard === 'mastercard' }"
                            @click="selectCardType('mastercard')">
                            <img src="https://upload.wikimedia.org/wikipedia/commons/b/b7/MasterCard_Logo.svg"
                                alt="MasterCard">
                        </div>
                    </div>
                    <div v-if="selectedCard" class="payment-details">
                        <form>
                            <div class="form-group">
                                <label for="cardNumber">Numéro de carte</label>
                                <input type="text" class="form-control" id="cardNumber" v-model="formattedCardNumber"
                                    placeholder="xxxx-xxxx-xxxx-xxxx" maxlength="19" required>
                            </div>
                            <div class="form-group">
                                <label for="cardName">Nom du titulaire</label>
                                <input type="text" class="form-control" id="cardName"
                                    placeholder="Entrez le nom du titulaire" required>
                            </div>
                            <div class="form-group">
                                <label for="expiryDate">Date d'expiration</label>
                                <input type="text" class="form-control" id="expiryDate" v-model="formattedExpiryDate"
                                    placeholder="MM/AA" maxlength="5" required>
                            </div>
                            <div class="form-group">
                                <label for="cvv">CVV</label>
                                <input type="text" class="form-control" id="cvv" v-model="cvv" placeholder="Entrez le CVV"
                                    maxlength="3" required>
                            </div>
                            <button type="submit" class="btn btn-primary btn-block mt-3">Payer maintenant</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, onMounted, ref, computed } from 'vue';

export default defineComponent({
    setup() {
        const trotinette = ref(null);
        const reservationDate = ref('');
        const reservationTime = ref('');
        const reservationDuration = ref(0);
        const dropOutLocation = ref('');
        const totalCost = ref(0);
        const userId = ref(0);
        const selectedCard = ref('');
        const cardNumber = ref('');
        const expiryDate = ref('');
        const cvv = ref('');

        onMounted(() => {
            const reservationDetails = JSON.parse(localStorage.getItem('reservationDetails') as string);
            if (reservationDetails) {
                trotinette.value = reservationDetails.trotinette;
                reservationDate.value = reservationDetails.reservationDate;
                reservationTime.value = reservationDetails.reservationTime;
                reservationDuration.value = reservationDetails.reservationDuration;
                dropOutLocation.value = reservationDetails.dropOutLocation;
                totalCost.value = reservationDetails.totalCost;
                userId.value = reservationDetails.user_id;
            }
        });

        const selectCardType = (type: string) => {
            selectedCard.value = type;
            cardNumber.value = '';
        };

        const formattedCardNumber = computed({
            get: () => cardNumber.value,
            set: (value: string) => {
                let formattedValue = value.replace(/\D/g, '');
                if (selectedCard.value === 'visa' && !formattedValue.startsWith('4')) {
                    formattedValue = '4' + formattedValue.slice(0, 15);
                } else if (selectedCard.value === 'mastercard' && !formattedValue.startsWith('5')) {
                    formattedValue = '5' + formattedValue.slice(0, 15);
                } else {
                    formattedValue = formattedValue.slice(0, 16);
                }
                cardNumber.value = formattedValue.replace(/(.{4})/g, '$1 ').trim();
            }
        });

        const formattedExpiryDate = computed({
            get: () => expiryDate.value,
            set: (value: string) => {
                let formattedValue = value.replace(/\D/g, '');
                if (formattedValue.length > 2) {
                    formattedValue = formattedValue.slice(0, 2) + '/' + formattedValue.slice(2, 4);
                }
                const parts = formattedValue.split('/');
                if (parts[0]) {
                    let month = parseInt(parts[0], 10);
                    if (month < 1) {
                        month = 1;
                    } else if (month > 12) {
                        month = 12;
                    }
                    parts[0] = month < 10 ? '0' + month : '' + month;
                }
                if (parts[1]) {
                    const currentYear = new Date().getFullYear() % 100; // Get last two digits of current year
                    let year = parseInt(parts[1], 10);
                    if (year < currentYear) {
                        year = currentYear;
                    }
                    parts[1] = year < 10 ? '0' + year : '' + year;
                }
                expiryDate.value = parts.join('/');
            }
        });

        return {
            trotinette,
            reservationDate,
            reservationTime,
            reservationDuration,
            dropOutLocation,
            totalCost,
            userId,
            selectedCard,
            cardNumber,
            expiryDate,
            cvv,
            selectCardType,
            formattedCardNumber,
            formattedExpiryDate,
        };
    },
});
</script>
  
<style scoped>
.trotinette-image {
    width: 60px;
    height: 60px;
}

.reservation-details p {
    background-color: #f8f9fa;
    padding: 10px;
    margin-bottom: 10px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.reservation-details p span {
    margin-left: auto;
}

.payment-form {
    background-color: #f8f9fa;
    padding: 20px;
    height: 100vh;
    box-shadow: -2px 0 5px rgba(0, 0, 0, 0.1);
}

.payment-form h2 {
    margin-bottom: 20px;
}

.payment-form .btn-block {
    width: 100%;
}

.card-selection {
    display: flex;
    justify-content: space-around;
    margin-bottom: 20px;
}

.card-selection div {
    width: 50%;
    text-align: center;
    cursor: pointer;
    padding: 10px;
    border: 2px solid transparent;
    border-radius: 5px;
}

.card-selection div:hover {
    background-color: lightgray;
}

.card-selection div.selected {
    border: 2px solid #007bff;
}

.card-selection img {
    width: 50px;
}

.payment-details {
    border: 2px solid #007bff;
    padding: 15px;
    margin-top: 15px;
    border-radius: 5px;
}
</style>
  