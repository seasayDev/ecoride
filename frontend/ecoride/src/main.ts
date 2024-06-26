import './assets/main.css'
import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import { RegisterUser } from './components/register/register'
import { LoginUser } from './components/login/login'
import { ResetPassword } from '@/components/resetPassword/resetPassword'
const app = createApp(App)

app.use(router)
app.provide('regitsre', new RegisterUser('http://127.0.0.1:5000/register'))
app.provide('loginUser', new LoginUser('http://127.0.0.1:5000'))
app.provide('resetPassword', new ResetPassword('http://127.0.0.1:5000'))
app.mount('#app')
