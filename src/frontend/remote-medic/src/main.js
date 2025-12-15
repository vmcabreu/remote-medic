import { createApp } from 'vue'
import './assets/styles/main.css'
import './assets/styles/icons.css'
import { createPinia } from 'pinia'
import PrimeVue from 'primevue/config'
import ToastService from 'primevue/toastservice'
import Toast from 'primevue/toast'
import App from './App.vue'
import router from './router' 
// Crear la aplicación Vue
const app = createApp(App)
app.use(PrimeVue)
app.use(ToastService)
app.component('AppToast', Toast)
// Configurar Pinia (para el manejo de estado)
const pinia = createPinia()
app.use(pinia)

// Configurar Vue Router
app.use(router)

// Montar la aplicación
app.mount('#app')
