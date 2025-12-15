import axios from "axios";
import { useAuthStore } from "@/stores/auth.store";

const API_BASE_URL = process.env.VUE_APP_API_URL || "http://localhost:5000";

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
const authStore = useAuthStore()
  const token = authStore.token?.value || sessionStorage.getItem('authToken')
  
  const publicRoutes = ["/api/auth/login", "/api/auth/register"]
  
  if (token && !publicRoutes.includes(config.url)) {
    config.headers["Authorization"] = `Bearer ${token}`
  }

  return config
}, (error) => {
  return Promise.reject(error)
})

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const authStore = useAuthStore()
      authStore.logout()
    }
    return Promise.reject(error)
  }
)


export default apiClient;
