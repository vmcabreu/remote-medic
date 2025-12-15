import apiClient from './apiClient'

const authService = {
  async register(user) {
    const response = await apiClient.post('/api/auth/register', user)
    return response.data
  },

  async login(user) {
    const response = await apiClient.post('/api/auth/login', {
      username: user.username,
      password: user.password
    })
    return response.data
  },

  async getUserData() {
    const response = await apiClient.get('/api/auth/me')
    return response.data
  }

}

export default authService