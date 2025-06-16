import axios from 'axios'

// Configuración base de Axios
const API_BASE_URL = process.env.VUE_APP_API_URL || 'http://localhost:5000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000, // 10 segundos timeout
})

// Interceptor para manejar errores globalmente
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message)
    return Promise.reject(error)
  }
)

export const patientService = {
  // Obtener todos los pacientes
  async getAllPatients(page = null, perPage = null) {
    try {
      const params = {}
      if (page) params.page = page
      if (perPage) params.per_page = perPage
      
      const response = await apiClient.get('/api/patients', { params })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener pacientes')
    }
  },

  // Obtener paciente por ID
  async getPatientById(id) {
    try {
      const response = await apiClient.get(`/api/patients/${id}`)
      return response.data.patient
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener paciente')
    }
  },

  // Crear nuevo paciente
  async createPatient(patientData) {
    try {
      const response = await apiClient.post('/api/patients', patientData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al crear paciente')
    }
  },

  // Actualizar paciente
  async updatePatient(id, patientData) {
    try {
      const response = await apiClient.put(`/api/patients/${id}`, patientData)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al actualizar paciente')
    }
  },

  // Eliminar paciente
  async deletePatient(id) {
    try {
      const response = await apiClient.delete(`/api/patients/${id}`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al eliminar paciente')
    }
  },

  // Asignar paciente a usuario
  async assignPatientToUser(patientId, userId) {
    try {
      const response = await apiClient.post(`/api/patients/${patientId}/assign`, {
        user_id: userId
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al asignar paciente')
    }
  },

  // Remover asignación
  async removePatientFromUser(patientId, userId) {
    try {
      const response = await apiClient.delete(`/api/patients/${patientId}/assign`, {
        data: { user_id: userId }
      })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al remover asignación')
    }
  },

  // Obtener usuarios asignados a un paciente
  async getPatientUsers(patientId) {
    try {
      const response = await apiClient.get(`/api/patients/${patientId}/users`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener usuarios')
    }
  },

  // Obtener pacientes de un usuario
  async getUserPatients(userId) {
    try {
      const response = await apiClient.get(`/api/users/${userId}/patients`)
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener pacientes del usuario')
    }
  }
}