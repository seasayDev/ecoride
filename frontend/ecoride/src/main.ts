import './assets/main.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import { RegisterUser } from './components/register/register'
const app = createApp(App)

app.use(router)
app.provide('regitsre', new RegisterUser('http://127.0.0.1:5000/register'))
app.mount('#app')
