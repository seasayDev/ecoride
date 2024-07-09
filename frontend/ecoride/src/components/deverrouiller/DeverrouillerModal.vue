<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Déverrouiller trottinette</h5>
                </div>
                <div class="modal-body">
                    <p>Un code de déverrouillage a été envoyé à votre adresse email. Veuillez entrer le code ci-dessous pour déverrouiller la trottinette.</p>
                    <input type="text" v-model="state.code" class="form-control" placeholder="Entrez le code de déverrouillage">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-primary" @click="validerCode">Valider</button>
                    <button type="button" class="btn btn-secondary" @click="closeModal">Fermer</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, reactive } from 'vue'
import axios from 'axios'

export default defineComponent({
    props: {
        isVisible: {
            type: Boolean as PropType<boolean>,
            required: true
        },
        trotinette: {
            type: Object as PropType<any>,
            required: true
        }
    },
    emits: ['close', 'codeSent'],
    setup(props, { emit }) {
        const state = reactive({
            code: ''
        })

        const closeModal = () => {
            emit('close')
        }

        const validerCode = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:5000/validateUnlockCode', {
                    code: state.code,
                    trotinetteId: props.trotinette.id_trotinette
                })
                if (response.data.success) {
                    emit('codeSent')
                    closeModal()
                } else {
                    alert('Code invalide. Veuillez réessayer.')
                }
            } catch (error) {
                alert('Erreur lors de la validation du code.')
            }
        }

        return {
            state,
            closeModal,
            validerCode
        }
    }
})
</script>

<style scoped>
.modal {
    display: flex;
    align-items: center;
    justify-content: center;
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
}
</style>
