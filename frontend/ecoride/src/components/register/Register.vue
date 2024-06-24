<template>
    <div class="container mt-5">
        <div class="alert alert-danger" role="alert" v-if="state.error">
            User already existe!
        </div>
        <form @submit.prevent="submitForm">
            <div class="row mb-3">
                <div class="col-md-4">
                    <label for="firstName" class="form-label">Nom :</label>
                    <input type="text" class="form-control" id="firstName" placeholder="Entrez votre nom"
                        v-model="state.model.firstName" required>
                </div>
                <div class="col-md-4">
                    <label for="lastName" class="form-label">Prénom :</label>
                    <input type="text" class="form-control" id="lastName" placeholder="Entrez votre prénom"
                        v-model="state.model.lastName" required>
                </div>
                <div class="col-md-4">
                    <label for="country" class="form-label">Pays de résidence :</label>
                    <input type="text" class="form-control" id="country" placeholder="Entrez votre pays"
                        v-model="state.model.country" required>
                </div>
            </div>
            <div class="mb-3">
                <label for="address" class="form-label">Addresse :</label>
                <input type="text" class="form-control" id="address" placeholder="Entrez votre nom"
                    v-model="state.model.address" required>
            </div>
            <div class="row mb-3">
                <div class="col-md-4">
                    <label for="city" class="form-label">Ville :</label>
                    <input type="text" class="form-control" id="city" placeholder="Entrez votre nom"
                        v-model="state.model.city" required>
                </div>
                <div class="col-md-4">
                    <label for="province" class="form-label">Province :</label>
                    <input type="text" class="form-control" id="province" placeholder="Entrez votre prénom"
                        v-model="state.model.province" required>
                </div>
                <div class="col-md-4">
                    <label for="postalCode" class="form-label">Code postale :</label>
                    <input type="text" class="form-control" id="postalCode" placeholder="Entrez votre pays"
                        v-model="state.model.postalCode" required>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="birthdate" class="form-label">Date de naissance :</label>
                    <input type="date" class="form-control" id="birthdate" placeholder="dd/mm/yyyy"
                        v-model="state.model.birthdate" required>
                </div>
                <div class="col-md-6">
                    <label for="email" class="form-label">Adresse courriel :</label>
                    <input type="email" class="form-control" id="email" placeholder="Entrez votre adresse courriel"
                        v-model="state.model.email" required>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="phone" class="form-label">Numéro de téléphone :</label>
                    <input type="tel" class="form-control" id="phone" placeholder="Entrez votre numéro de téléphone"
                        v-model="state.model.phone" required>
                </div>
            </div>
            <div class="row mb-3">
                <div class="col-md-6">
                    <label for="password" class="form-label">Mot de passe :</label>
                    <input type="password" class="form-control" id="password" placeholder="Choisissez un mot de passe"
                        v-model="state.model.password" required>
                </div>
                <div class="col-md-6">
                    <label for="confirmPassword" class="form-label">Répétez votre mot de passe :</label>
                    <input type="password" class="form-control" id="confirmPassword"
                        placeholder="Répétez votre mot de passe" v-model="state.model.confirmPassword" required>
                </div>
            </div>
            <button type="submit" class="btn btn-dark">S'inscrire</button>
        </form>
    </div>
</template>
<script lang="ts">
import { defineComponent, inject, reactive } from 'vue'
import { register, RegisterUser } from './register'

export default defineComponent({
    name: 'Register',
    setup() {
        const registerUser = inject('regitsre') as RegisterUser;
        const state = reactive({
            model: {} as register,
            error: false,

        })
        const submitForm = async () => {
            try {
                const register = await registerUser.registerUser(state.model);
                console.log("REGISTER", register)
            } catch (e) {
                state.error = true;
            }
        }

        return {
            state,
            registerUser,
            submitForm
        }

    },
})
</script>
<style scoped>
.container {
    background-color: #778da9;
    padding: 20px;
    border-radius: 8px;
}
</style>
