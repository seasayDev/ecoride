<template>
    <div class="container mt-5">
        <form @submit.prevent="submitForm" class="reset-form">
            <h2>Réinitialisé le mot de passe</h2>
            <span>Votre mot de passe vous sera envoyé par email</span>
            <div class="form-group">
                <label for="inputEmail">Adresse électronique</label>
                <input type="email" class="form-control" id="inputEmail" aria-describedby="emailHelp"
                    placeholder="Entrez l'email" v-model="state.email">
            </div>
            <button type="submit" class="btn btn-primary">Soumettre</button>
        </form>
    </div>
</template>
<script lang="ts">
import { defineComponent, reactive } from 'vue'

export default defineComponent({
    name: "ResetPassword",
    setup() {
        const state = reactive({
            email: ''
        })

        const submitForm = () => {
            console.log('reste form')
        }

        return {
            state,
            submitForm
        }


    },
})
</script>

<style scoped>
.reset-form {
    padding: 2rem;
    background-color: var(--blue-light);
    border-radius: 0.5rem;
}

.btn {
    margin-top: 2rem;


}
</style>
