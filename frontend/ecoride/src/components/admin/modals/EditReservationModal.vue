<template>
    <div class="reservation-modal" v-if="isVisible">
        <div class="container">
            <form @submit.prevent="editReservation">
                <button class="close-button" @click="closeEditModal"><i class="bi bi-x-circle"></i></button>
                <div class="row mb-3 mt-5">
                    <div class="col-md-4">
                        <label for="firstName" class="form-label">User First Name</label>
                        <input type="text" class="form-control" id="firstName" v-model="state.reservation.user.first_name"
                            placeholder="Enter First Name" required>
                    </div>
                    <div class="col-md-4">
                        <label for="lastName" class="form-label">User Last Name</label>
                        <input type="text" class="form-control" id="lastName" v-model="state.reservation.user.last_name"
                            placeholder="Enter Last Name" required>
                    </div>
                    <div class="col-md-4">
                        <label for="trotinetteModel" class="form-label">Trotinette Model</label>
                        <input type="text" class="form-control" id="trotinetteModel"
                            v-model="state.reservation.trotinette.model" placeholder="Enter Trotinette Model" required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="category" class="form-label">Trotinette Category</label>
                        <input type="text" class="form-control" id="category"
                            v-model="state.reservation.trotinette.category" placeholder="Enter Trotinette Category"
                            required>
                    </div>
                    <div class="col-md-4">
                        <label for="pickUpLocation" class="form-label">Pick Up Location</label>
                        <input type="text" class="form-control" id="pickUpLocation"
                            v-model="state.reservation.pick_up_location.name" placeholder="Enter Pick Up Location" required>
                    </div>
                    <div class="col-md-4">
                        <label for="dropOffLocation" class="form-label">Drop Off Location</label>
                        <input type="text" class="form-control" id="dropOffLocation"
                            v-model="state.reservation.drop_off_location.name" placeholder="Enter Drop Off Location"
                            required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="startDate" class="form-label">Start Date</label>
                        <input type="date" class="form-control" id="startDate" v-model="state.reservation.start_date"
                            required>
                    </div>
                    <div class="col-md-4">
                        <label for="endDate" class="form-label">End Date</label>
                        <input type="date" class="form-control" id="endDate" v-model="state.reservation.end_date" required>
                    </div>
                    <div class="col-md-4">
                        <label for="reservationHours" class="form-label">Reservation Hours</label>
                        <input type="number" class="form-control" id="reservationHours"
                            v-model="state.reservation.reservation_hours" placeholder="Enter Reservation Hours" required>
                    </div>
                </div>
                <div class="row mb-3">
                    <div class="col-md-4">
                        <label for="totalCost" class="form-label">Total Cost</label>
                        <input type="number" class="form-control" id="totalCost" v-model="state.reservation.total_cost"
                            placeholder="Enter Total Cost" required>
                    </div>
                </div>
                <button type="submit" class="btn btn-primary mt-5">Submit</button>
            </form>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, PropType, reactive, watch, inject } from 'vue'
import { GetTrotinettes } from '../admin'

export default defineComponent({
    props: {
        isVisible: {
            type: Boolean as PropType<boolean>,
            required: true,
        },
        reservation: {
            type: Object as PropType<any>,
            required: true
        }
    },
    emits: ['close', 'update'],
    setup(props, { emit }) {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const state = reactive({
            reservation: { ...props.reservation }
        })

        watch(() => props.reservation, (newValue) => {
            state.reservation = { ...newValue }
        }, { immediate: true })

        const closeEditModal = (event: Event) => {
            event.preventDefault();
            event.stopPropagation();
            emit('close');
        };

        const editReservation = async () => {
            const result = { ...state.reservation };
            //await trotinettes.updateReservation(result)
            emit('update', state.reservation);
            emit('close');
        }

        return {
            closeEditModal,
            state,
            editReservation,
            trotinettes
        };
    },
})
</script>
  
<style scoped>
.reservation-modal {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    align-items: center;
    justify-content: center;
    background-color: rgba(0, 0, 0, 0.5);
    z-index: 1000;
}

.container {
    background-color: white;
    padding: 20px;
    border-radius: 8px;
    text-align: center;
    position: relative;
}

.close-button {
    position: absolute;
    top: 10px;
    right: 10px;
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
}

.bi {
    color: red;
}

.bi:hover {
    color: blue;
}
</style>
  