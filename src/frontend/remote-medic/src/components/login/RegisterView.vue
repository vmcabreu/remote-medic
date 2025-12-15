<script>
import { reactive } from 'vue';
import authService from './../../services/authService'

export default {
  name: 'RegisterView',
  emits: ['login', 'error'],
  setup(props, { emit }) {
    const user = reactive({
      username: '',
      firstName: '',
      lastName: '',
      email: '',
      phone: '',
      password: '',
      repeatPassword: ''
    });

    const doRegister = async () => {
      try {
    if (user.password !== user.repeatPassword) {
      emit('error', 'Las contraseñas no coinciden');
      return;
    }
        const registerData = {
      username: user.username.trim(),
      email: user.email.trim(),
      password: user.password,
      first_name: user.firstName.trim(),
      last_name: user.lastName.trim(),
      phone: user.phone.trim()  // ✅ AGREGADO phone
    };
        await authService.register(registerData);
        emit('login');
      } catch (err) {
        const message = err.response?.data?.error || 'Error al registrarse';
        emit('error', message);
      }
    };

    const changeToLogin = () => emit('login');

    return { user, doRegister, changeToLogin };
  }
}
</script>

<template>
  <div class="register-form">    
    <div class="form-header">
      <h3 class="form-title">Registro</h3>
      <p class="form-subtitle">Completa todos los campos</p>
    </div>
    
    <form @submit.prevent="doRegister" class="form-stack">
      
      <div class="input-row">
        <div class="input-group">
          <label class="input-label">Nombres</label>
          <div class="input-wrapper">
            <input v-model.trim="user.firstName" type="text" class="form-input" placeholder="Juan"
              autocomplete="given-name">
          </div>
        </div>
        <div class="input-group">
          <label class="input-label">Apellidos</label>
          <div class="input-wrapper">
            <input v-model.trim="user.lastName" type="text" class="form-input" placeholder="Pérez García"
              autocomplete="family-name">
          </div>
        </div>
      </div>
      
      <div class="input-row">
        <div class="input-group">
          <label class="input-label">Usuario</label>
          <div class="input-wrapper">
            <input v-model.trim="user.username" type="text" class="form-input" placeholder="juan.medico23"
              autocomplete="username">
          </div>
        </div>
        <div class="input-group">
          <label class="input-label">Email</label>
          <div class="input-wrapper">
            <input v-model.trim="user.email" type="email" class="form-input" placeholder="juan@clinicamedica.com"
              autocomplete="email">
          </div>
        </div>
      </div>
      
      <div class="input-group full-width">
        <label class="input-label">Teléfono</label>
        <div class="input-wrapper">
          <input v-model.trim="user.phone" type="tel" class="form-input" placeholder="+34 612 345 678"
            autocomplete="tel">
        </div>
      </div>
      
      <div class="input-row">
        <div class="input-group">
          <label class="input-label">Contraseña</label>
          <div class="input-wrapper">
            <input v-model.trim="user.password" type="password" class="form-input" placeholder="Mínimo 8 caracteres"
              autocomplete="new-password">
          </div>
        </div>
        <div class="input-group">
          <label class="input-label">Confirmar</label>
          <div class="input-wrapper">
            <input v-model.trim="user.repeatPassword" type="password" class="form-input"
              placeholder="Repite tu contraseña" autocomplete="new-password">
          </div>
        </div>
      </div>
    </form>
    
    <div class="form-actions">
      <button class="btn-primary btn-large" type="submit" @click="doRegister">
        Crear Mi Cuenta
      </button>
      <button class="btn-secondary btn-large" type="button" @click="changeToLogin">
        Ya tengo cuenta
      </button>
    </div>
  </div>
</template>

<style scoped>
.register-form {
  width: 100%;
  animation: formSlideUp 0.8s cubic-bezier(0.25, 0.46, 0.45, 0.94);
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

.input-row {
  display: grid;
  position: relative;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  width: 400px;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.input-group.full-width {
  grid-column: 1 / -1;
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
  color: #9ca3af;
  font-size: 1.2rem;
  z-index: 2;
}

.form-input {
  width: 100%;
  padding: 8px 10px 8px 10px;
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

.form-input:focus~.input-icon {
  color: #38aa77 !important;
}

.form-actions {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.btn-primary,
.btn-secondary {
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
}

.btn-primary:hover {
  transform: translateY(-4px);
  box-shadow: 0 24px 60px rgba(56, 170, 119, 0.55);
}

.btn-secondary {
  background: rgba(17, 20, 24, 0.7);
  color: #e2e8f0;
  border: 2px solid rgba(56, 170, 119, 0.4);
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
    transform: translateY(40px) scale(0.97);
  }

  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Responsive PERFECTO */
@media (max-width: 768px) {
  .input-row {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .form-input {
    height: 60px;
    padding: 18px 20px 18px 56px;
    font-size: 1rem;
  }

  .btn-primary,
  .btn-secondary {
    height: 60px;
    padding: 18px 28px;
    font-size: 1rem;
  }

  .form-title {
    font-size: 1.7rem;
  }
}
</style>
