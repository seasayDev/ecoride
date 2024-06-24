<template>
    <div>
        <div class="alert alert-danger" role="alert" v-if="state.error">
            Mot de passe incorrect !
        </div>
        <div class="container">
            <div class="row justify-content-center">
                <form @submit.prevent="submit()" class="login_form">
                    <div class="form-group">
                        <label for="inputEmail">Adresse électronique</label>
                        <input type="email" class="form-control" id="inputEmail" aria-describedby="emailHelp"
                            placeholder="Entrez l'email" v-model="state.model.email">
                    </div>
                    <div class="form-group">
                        <label for="inputPassword1">Mot de passe</label>
                        <input type="password" class="form-control" id="inputPassword1" placeholder="Mot de passe"
                            v-model="state.model.password">
                    </div>
                    <button type="submit" class="btn btn-primary">Soumettre</button>
                    <div>
                        <div class="register" @click="register">s'inscrire</div>
                        <div class="resetPassword" @click="resetPassword">Mot de passe oublie?</div>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, inject, reactive } from 'vue'
import { loginModel, LoginUser } from './login';
import { useRouter } from "vue-router";
import { setUser } from '../helpers/userSession';
export default defineComponent({
    name: 'Login',
    setup() {
        const loginUser = inject('loginUser') as LoginUser;
        const router = useRouter();
        const state = reactive({
            model: {} as loginModel,
            error: false
        })

        const submit = async () => {
            try {
                const user = await loginUser.connexion(state.model);
                setUser(user)
                router.push('/')
            } catch (e) {
                state.error = true;
            }

        }
        const resetPassword = () => {
            router.push('/resetPassword')
        }
        const register = () => {
            router.push('/register')
        }

        return {
            state,
            submit,
            register,
            loginUser,
            resetPassword
        }

    },
})
</script>
<style scoped>
.container {
    display: flex;
    align-items: center;
    justify-content: center;
    min-height: 100vh;

}

.login_form {
    background: var(--cyan-blue);
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
    color: white;
    box-shadow: 0px 0px 16px 3px rgba(0, 0, 0, 0.53);
}

.form-group {
    padding-bottom: 1rem;
}

.btn {
    width: 100%;
    margin-top: 1rem;
}

.register {
    margin-top: 1rem;
    text-align: right;
}

.register:hover {
    text-decoration: underline;
    cursor: pointer;
}

.resetPassword:hover {
    text-decoration: underline;
    cursor: pointer;
}
</style>
