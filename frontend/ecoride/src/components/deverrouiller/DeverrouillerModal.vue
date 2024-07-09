<template>
    <div class="modal" v-if="isVisible">
        <div class="modal-dialog" role="document">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Déverrouiller trottinette</h5>
                </div>
                <div class="modal-body">
                    <div v-if="!codeSent">
                        <p>Entrez votre email pour recevoir le code de déverrouillage :</p>
                        <input type="email" v-model="state.email" class="form-control" placeholder="Entrez votre email">
                        <button type="button" class="btn btn-primary mt-2" @click="sendUnlockCode">Envoyer</button>
                    </div>
                    <div v-else>
                        <p>Un code de déverrouillage a été envoyé à votre adresse email. Veuillez entrer le code ci-dessous pour déverrouiller la trottinette.</p>
                        <input type="text" v-model="state.code" class="form-control" placeholder="Entrez le code de déverrouillage">
                        <button type="button" class="btn btn-primary mt-2" @click="validerCode">Valider</button>
                    </div>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="closeModal">Fermer</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent, PropType, reactive, ref } from 'vue'
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
            email: '',
            code: ''
        })
        const codeSent = ref(false)

        const closeModal = () => {
            emit('close')
        }

        const sendUnlockCode = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:5000/sendUnlockCode', {
                    email: state.email,
                    trotinette_id: props.trotinette.id_trotinette
                })
                if (response.data.success) {
                    codeSent.value = true
                } else {
                    alert('Erreur lors de l\'envoi du code. Veuillez réessayer.')
                }
            } catch (error) {
                alert('Erreur lors de l\'envoi du code.')
            }
        }

        const validerCode = async () => {
            try {
                const response = await axios.post('http://127.0.0.1:5000/validateUnlockCode', {
                    code: state.code,
                    trotinette_id: props.trotinette.id_trotinette
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
            codeSent,
            closeModal,
            sendUnlockCode,
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
