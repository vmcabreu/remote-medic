import { createRouter, createWebHistory } from 'vue-router'

// Importar componentes de página
import LoginLayout from '@/components/layout/login/LoginLayout.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: LoginLayout
  },
  {
    path: '/login',
    name: 'Login',
    component: LoginLayout
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router