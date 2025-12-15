<script>
import { ref, onMounted } from 'vue'
import authService from './../../services/authService'
import { useAuthStore } from '@/stores/auth.store'

export default {
  name: 'ProfilePage',
  setup() {
    const profile = ref(null)
    const authStore = useAuthStore()
    const isLoading = ref(false)

    const fetchProfile = async () => {
      try {
        isLoading.value = true
        const response = await authService.getUserData()
        profile.value = response
      } catch (err) {
        console.error('Error al cargar perfil:', err)
      } finally {
        isLoading.value = false
      }
    }
const formatWorkDays = (workDays) => {
  if (!workDays) return 'No definido';
  
  const daysMap = {
    'mon': 'Lunes',
    'tue': 'Martes', 
    'wed': 'Miércoles',
    'thu': 'Jueves',
    'fri': 'Viernes'
  };
  
  return workDays.split(',')
    .map(day => daysMap[day.trim()] || day)
    .filter(Boolean)
    .join(', ');
}
    const formatDate = (dateStr) => {
      const date = new Date(dateStr)
      const year = date.getFullYear()
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const day = String(date.getDate()).padStart(2, '0')
      const hours = String(date.getHours()).padStart(2, '0')
      const minutes = String(date.getMinutes()).padStart(2, '0')
      const seconds = String(date.getSeconds()).padStart(2, '0')

      return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`
    }
    onMounted(fetchProfile)
    return {
      profile,
      authStore,
      isLoading,
      formatDate,
      formatWorkDays
    }
  }
}
</script>

<template>
  <div class="profile-container">
    <div class="profile-hero">
      <div class="profile-avatar">
        <i class="core-icon circle-user big-icon"></i>
      </div>
      <div class="profile-info">
        <h1 class="profile-name">{{ profile?.full_name || 'Doctor' }}</h1>
      </div>
    </div>

    <div class="stats-grid" v-if="profile">
      <div class="stat-card">
        <div class="stat-number">{{ profile.patient_count || 0 }}</div>
        <div class="stat-label">Pacientes</div>
      </div>
      <div class="stat-card">
        <div class="stat-number">{{ profile.in_working_hours ? 'Disponible' : 'No disponible'  || 'No disponible' }}</div>
        <div class="stat-label">Disponibilidad</div>
      </div>
    </div>

    <div class="profile-details">
      <h3 class="section-title">Información Personal</h3>
      <div class="detail-grid">
        <div class="detail-item">
          <label>Email</label>
          <span>{{ profile?.email }}</span>
        </div>
        <div class="detail-item">
          <label>Teléfono</label>
          <span>{{ profile?.phone || 0 }}</span>
        </div>
        <div class="detail-item">
          <label>Días disponibles</label>
          <span>{{formatWorkDays(profile?.work_days) || "Ninguno"}}</span>
        </div>
        <div class="detail-item">
          <label>Fecha Registro</label>
          <span>{{ formatDate(profile?.created_at) }}</span>
        </div>
      </div>
    </div>

    <div class="profile-actions">
      <button class="action-btn primary" @click="authStore.logout">
        Cerrar Sesión
      </button>
    </div>

    <div v-if="isLoading" class="loading-overlay">
      <div class="spinner"></div>
    </div>
  </div>
</template>

<style scoped>
.profile-container {
  background: #1a1e23;
  padding: 30px;
  border-radius: 12px;
  color: #cfd3dc;
  font-family: Inter, sans-serif;
  min-height: 100%;
}

.profile-hero {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #222;
}

.profile-avatar {
  width: 80px;
  height: 80px;
  background: linear-gradient(135deg, #38aa77, #51f7ac);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: white;
}

.profile-info h1 {
  color: #fff;
  font-size: 1.8rem;
  margin: 0 0 5px 0;
  font-weight: 700;
}

.profile-role {
  color: #38aa77;
  font-size: 1rem;
  margin: 0;
  font-weight: 500;
}

.profile-badge {
  display: inline-block;
  background: #38aa77;
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.8rem;
  margin-top: 8px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #111418;
  padding: 20px;
  border-radius: 10px;
  text-align: center;
  border: 1px solid #222;
  transition: transform 0.2s;
}

.stat-card:hover {
  transform: translateY(-2px);
}

.stat-number {
  font-size: 2rem;
  font-weight: 700;
  color: #fff;
  display: block;
}

.stat-label {
  color: #38aa77;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.profile-details {
  background: #111418;
  border-radius: 10px;
  padding: 25px;
  border: 1px solid #222;
  margin-bottom: 20px;
}

.section-title {
  color: #fff;
  font-size: 1.3rem;
  display: flex;
  margin-bottom: 20px;
  padding-left: 10px;
  border-left: 4px solid #38aa77;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.detail-item {
  display: flex;
  flex-direction: column;
}

.detail-item label {
  color: #38aa77;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 5px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.detail-item span {
  color: #cfd3dc;
  font-size: 1rem;
}

.profile-actions {
  display: flex;
  gap: 15px;
  justify-content: center;
}

.action-btn {
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.25s;
  border: none;
  font-family: Inter, sans-serif;
}

.action-btn.primary {
  background: #111418;
  color: #38aa77;
  border: 1px solid #38aa77;
}

.action-btn.primary:hover {
  background: #38aa77;
  color: white;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(26, 30, 35, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 12px;
}

.spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #222;
  border-top: 3px solid #38aa77;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

@media (max-width: 768px) {
  .profile-hero {
    flex-direction: column;
    text-align: center;
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>
