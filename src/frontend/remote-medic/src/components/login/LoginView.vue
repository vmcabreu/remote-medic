<script>
import { reactive } from "vue";
import authService from './../../services/authService'
import { useAuthStore } from '@/stores/auth.store'
export default {
  name: 'LoginView',
  emits: ['register', 'error', 'redirect'],
   setup(props, { emit }) { 
    const authStore = useAuthStore()
    const user = reactive({
      username: '',
      password: ''
    })
    const doLogin = async () => {
      try {
      const data = await authService.login(user)
      authStore.setToken(data.token)
      authStore.setUser(data.user)
       emit('redirect')
      } catch (err) {
        const message = err.response?.data?.error || 'Error al iniciar sesión'
        emit('error', message)
      }
    }
     const changeToRegister = () => emit('register')
    return {
      user,
      authStore,
      changeToRegister,
      doLogin
    }
  }
}
</script>
<template>
  <h4>Iniciar Sesión</h4>
  <div class="input-layout">
    <p>Usuario:</p>
    <input type="text" v-model.trim="user.username">
  </div>
  <div class="input-layout">
    <p>Contraseña:</p>
    <input type="password" v-model.trim="user.password">
  </div>
  <div class="flex">
    <button class="button-template button-success" @click="doLogin()">Login</button>
    <button class="button-template button-grey" @click="changeToRegister()">Registrarse</button>
  </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
