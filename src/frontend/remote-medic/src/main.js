import { createApp } from 'vue'
import './assets/styles/main.css'
import { createPinia } from 'pinia'
import App from './App.vue'
// Crear la aplicación Vue
const app = createApp(App)

// Configurar Pinia (para el manejo de estado)
const pinia = createPinia()
app.use(pinia)

// Configurar Vue Router
//app.use(router)

// Montar la aplicación
app.mount('#app')
