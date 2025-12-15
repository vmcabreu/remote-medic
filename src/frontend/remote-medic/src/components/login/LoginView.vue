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
  <div class="login-form">    
    <div class="form-header">
      <h3 class="form-title">Bienvenido</h3>
      <p class="form-subtitle">Accede a tu cuenta médica</p>
    </div>
    
    <form @submit.prevent="doLogin" class="form-stack">
            
      <div class="input-group">
        <div class="input-wrapper">
          <i class="core-icon user-avatar small-icon input-icon"></i>
          <input 
            v-model.trim="user.username" 
            type="text" 
            class="form-input"
            placeholder="Usuario"
            autocomplete="username"
          >
        </div>
      </div>
      
      <div class="input-group">
        <div class="input-wrapper">
          <i class="core-icon password small-icon input-icon"></i>
          <input 
            v-model.trim="user.password" 
            type="password" 
            class="form-input"
            placeholder="Contraseña"
            autocomplete="current-password"
          >
        </div>
      </div>
    </form>
    
    <div class="form-actions">
      <button class="btn-primary btn-large" type="submit" @click="doLogin">
        <i class="core-icon login-form-icon small-icon" ></i>
        Iniciar Sesión
      </button>
      <button class="btn-secondary btn-large" type="button" @click="changeToRegister">
        <i class="core-icon register-form-icon small-icon"></i>
        Crear cuenta
      </button>
    </div>
  </div>
</template>

<style scoped>
.login-form {
  width: 100%;
  animation: formSlideUp 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
  padding: 0 8px;
}

.form-header {
  text-align: center;
  margin-bottom: 40px;
}

.form-title {
  color: #fff;
  font-size: 2rem;
  font-weight: 700;
  margin: 0 0 12px;
  background: linear-gradient(135deg, #38aa77, #51f7ac);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.form-subtitle {
  color: #9ca3af;
  font-size: 1rem;
  margin: 0;
  font-weight: 400;
}

.form-stack {
  display: flex;
  flex-direction: column;
  gap: 28px;
  margin-bottom: 40px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-label {
  color: #e2e8f0;
  font-size: 0.95rem;
  font-weight: 500;
  letter-spacing: 0.01em;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 20px;
  background-color: #9ca3af;
  font-size: 1.2rem;
  z-index: 2;
}

.form-input {
  width: 100%;
  padding: 20px 24px 20px 60px;
  background: rgba(17, 20, 24, 0.85);
  border: 2px solid rgba(56, 170, 119, 0.25);
  border-radius: 20px;
  color: #fff;
  font-size: 1.05rem;
  font-weight: 400;
  backdrop-filter: blur(16px);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  outline: none;
  height: 64px;
  box-sizing: border-box;
}

.form-input::placeholder {
  color: #6b7280;
}

.form-input:focus {
  border-color: #38aa77;
  box-shadow: 
    0 0 0 4px rgba(56, 170, 119, 0.15),
    0 16px 40px rgba(56, 170, 119, 0.25);
  background: rgba(17, 20, 24, 0.98);
  transform: translateY(-2px);
}

.form-input:focus ~ .input-icon {
  color: #38aa77 !important;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.btn-primary, .btn-secondary {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  padding: 20px 32px;
  border: none;
  border-radius: 20px;
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
  height: 68px;
}

.btn-large {
  height: 68px;
  font-size: 1.1rem;
}

.btn-primary {
  background: linear-gradient(135deg, #38aa77 0%, #10b981 50%, #51f7ac 100%);
  color: white;
  box-shadow: 0 12px 35px rgba(56, 170, 119, 0.45);
  i{
    background-color: white;
  }
}

.btn-primary:hover:not(:disabled) {
  transform: translateY(-4px);
  box-shadow: 0 24px 60px rgba(56, 170, 119, 0.55);
}

.btn-secondary {
  background: rgba(17, 20, 24, 0.7);
  color: #e2e8f0;
  border: 2px solid rgba(56, 170, 119, 0.4);
    i{
    background-color: #e2e8f0;
  }
}

.btn-secondary:hover {
  background: rgba(56, 170, 119, 0.15);
  border-color: #38aa77;
  color: #fff;
  transform: translateY(-2px);
  box-shadow: 0 12px 30px rgba(56, 170, 119, 0.25);
}

@keyframes formSlideUp {
  from {
    opacity: 0;
    transform: translateY(30px) scale(0.97);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .form-input {
    height: 60px;
    padding: 18px 20px 18px 56px;
    font-size: 1rem;
  }
  
  .btn-primary, .btn-secondary {
    height: 60px;
    padding: 18px 28px;
    font-size: 1rem;
  }
  
  .form-title {
    font-size: 1.7rem;
  }
}
</style>
