<template>
    <div class="product-modal" v-if="isVisible">

        <div class="modal" tabindex="-1" role="dialog">
            <div class="modal-dialog" role="document">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Supprimer trottinette</h5>
                    </div>
                    <div class="modal-body">
                        <p>Êtes-vous sûr de vouloir supprimer ce produit ?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-danger" @click="deleteProduct">Supprimer</button>
                        <button type="button" class="btn btn-secondary" @click="closeModal">Close</button>
                    </div>
                </div>
            </div>
        </div>

    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, inject } from 'vue'
import { Trotinette, Location, Newscooter, GetTrotinettes } from '../admin'

export default defineComponent({
    props: {
        isVisible: {
            type: Boolean as PropType<boolean>,
            required: true,
        },
        trotinette: {
            type: {} as PropType<Trotinette>,
            required: true
        },
    },
    emits: ['close'],
    setup(props, { emit }) {
        const trotinettes = inject('getTrotinettes') as GetTrotinettes
        const closeModal = () => {
            emit('close');
        };

        return {
            closeModal,
            trotinettes

        };
    },
})
</script>

<style scoped>
.product-modal {
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
