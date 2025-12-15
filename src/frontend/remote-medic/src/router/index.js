import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import LoginLayout from '@/components/layout/login/LoginLayout.vue'
import MainLayout from '@/components/layout/main/MainLayout.vue'
import PatientTableView from '@/components/patient/PatientTableView.vue'
import ProfileView from '@/components/profile/ProfileView.vue'
import PatientDetailsView from '@/components/patient/PatientDetailsView.vue'
import MedicineTable from '@/components/medicine/MedicineTable.vue'
import DashboardLayout from '@/components/layout/main/DashboardLayout.vue'

const routes = [
  { path: '/login', name: 'Login', component: LoginLayout },
  { 
    path: '/', 
    name: 'Home', 
    component: MainLayout, 
    redirect: { name: 'Dashboard' },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: DashboardLayout,
        meta: { requiresAuth: true }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: ProfileView,
        meta: { requiresAuth: true }
      },
      {
        path: 'medicines',
        name: 'Medicines',
        component: MedicineTable,
        meta: { requiresAuth: true }
      },
      {
        path: 'patients',
        name: 'PatientList',
        component: PatientTableView,
        meta: { requiresAuth: true }
      },
      {
        path: 'patients/:id',
        name: 'PatientDetails',
        component: PatientDetailsView,
        meta: { requiresAuth: true }
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  }
  else if (to.path === '/login' && authStore.isAuthenticated) {
    next('/')
  }
  else {
    next()
  }
})

export default router
