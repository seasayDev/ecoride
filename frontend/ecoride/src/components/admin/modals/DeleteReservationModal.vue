<template>
    <div class="reservation-modal" v-if="isVisible">
        <div class="modal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Supprimer la réservation</h5>
                    </div>
                    <div class="modal-body">
                        <p>Êtes-vous sûr de vouloir supprimer cette réservation ?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" @click="deleteReservation">Supprimer</button>
                        <button type="button" class="btn btn-secondary" @click="closeModal">Fermer</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
  
<script lang="ts">
import { defineComponent, PropType, inject, reactive, watch } from 'vue'
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
    emits: ['close'],
    setup(props, { emit }) {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const state = reactive({
            reservation: { ...props.reservation }
        })

        watch(() => props.reservation, (newValue) => {
            state.reservation = { ...newValue }
        }, { immediate: true })

        const closeModal = () => {
            emit('close');
        };

        const deleteReservation = async () => {
            await trotinettes.deleteReservation(state.reservation.id_reservation)
            emit('close');
        }

        return {
            closeModal,
            deleteReservation,
            state
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

.modal {
    display: block;
}
</style>
  