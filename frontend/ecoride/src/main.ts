import './assets/main.css'
import './assets/base.css'

import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap/dist/js/bootstrap.bundle.js'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'jquery'
import { RegisterUser } from './components/register/register'
import { LoginUser } from './components/login/login'
import { ResetPassword } from '@/components/resetPassword/resetPassword'
import { ProfileService } from './components/profil/profil';

import { EditProfileService } from './components/editProfil/editprofil'
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser, faEnvelope, faPhone, faMapMarkerAlt, faCalendarAlt, faGlobe, faCity, faMap, faMailBulk, faPen } from '@fortawesome/free-solid-svg-icons'

// Add icons to the library
library.add(faUser, faEnvelope, faPhone, faMapMarkerAlt, faCalendarAlt, faGlobe, faCity, faMap, faMailBulk, faPen)
import { GetTrotinettes } from './components/admin/admin'
import { SupportService } from '@/components/support/support'

const app = createApp(App)
const backURL = 'http://127.0.0.1:5000' // back end url to send api requests

app.use(router)
app.provide('editProfil', new EditProfileService('http://127.0.0.1:5000'));
app.component('font-awesome-icon', FontAwesomeIcon)
app.provide('profileService', new ProfileService('http://localhost:5000/profil') );
app.provide('regitsre', new RegisterUser('http://127.0.0.1:5000/register'))
app.provide('loginUser', new LoginUser('http://127.0.0.1:5000'))
app.provide('resetPassword', new ResetPassword('http://127.0.0.1:5000'))
app.provide('regitsre', new RegisterUser(backURL + '/register'))
app.provide('loginUser', new LoginUser(backURL))
app.provide('resetPassword', new ResetPassword(backURL))
app.provide('getTrotinettes', new GetTrotinettes(backURL))
app.provide('supportService', new SupportService(backURL + '/support'))
app.mount('#app')
