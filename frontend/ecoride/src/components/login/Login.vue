<template>
    <div>
        <div class="alert alert-danger" role="alert" v-if="state.error">
            Wrong password !
        </div>
        <div class="container">
            <div class="row justify-content-center">
                <form @submit.prevent="submit()" class="login_form">
                    <div class="form-group">
                        <label for="inputEmail">Email address</label>
                        <input type="email" class="form-control" id="inputEmail" aria-describedby="emailHelp"
                            placeholder="Enter email" v-model="state.model.email">

                    </div>
                    <div class="form-group">
                        <label for="inputPassword1">Password</label>
                        <input type="password" class="form-control" id="inputPassword1" placeholder="Password"
                            v-model="state.model.password">
                    </div>
                    <button type="submit" class="btn btn-primary">Submit</button>
                    <div class="register" @click="register">register</div>
                </form>
            </div>
        </div>
    </div>
</template>
<script lang="ts">
import { defineComponent, inject, reactive } from 'vue'
import { loginModel, LoginUser } from './login';
import { useRouter } from "vue-router";
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
                await loginUser.connexion(state.model);
                router.push('/')
            } catch (e) {
                state.error = true;
            }

        }
        const register = () => {
            router.push('/register')
        }

        return {
            state,
            submit,
            register,
            loginUser
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
    background: #415a77;
    padding: 2rem;
    border-radius: 0.5rem;
    box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075);
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
</style>
