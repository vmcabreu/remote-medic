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
  async register(user) {
    try {
      const params = {}
      params.username=username
      params.email=email
      params.password=password
      
      const response = await apiClient.post('/api/auth/register', { params })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener pacientes')
    }
  },
  async register(username,email,password) {
    try {
      const params = {}
      params.username=username
      params.email=email
      params.password=password
      
      const response = await apiClient.post('/api/auth/register', { params })
      return response.data
    } catch (error) {
      throw new Error(error.response?.data?.error || 'Error al obtener pacientes')
    }
  },



}