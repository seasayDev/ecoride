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
const backURL = 'http://127.0.0.1:5000' // back end url to send  api requests
app.use(router)
app.provide('regitsre', new RegisterUser(backURL + '/register'))
app.provide('loginUser', new LoginUser(backURL))
app.provide('resetPassword', new ResetPassword(backURL))
app.mount('#app')
