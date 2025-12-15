<script>
import { ref } from 'vue'
import MessageToast from './../MessageToast.vue'
import LoginView from './../../login/LoginView.vue'
import RegisterView from './../../login/RegisterView.vue'
import { useRouter } from 'vue-router'

export default {
  name: 'LoginLayout',
  components: {
    LoginView,
    RegisterView,
    MessageToast
  },
  setup() {
    const loginFlag = ref(true)
    const toast = ref(null)
    const router = useRouter()

    const showError = (msg) => toast.value.show(msg)
    const setRegister = () => loginFlag.value = false
    const setLogin = () => loginFlag.value = true
    const redirectToMainPage = () => router.push({ name: 'Home' })

    return {
      loginFlag, setRegister, setLogin, toast, showError, redirectToMainPage
    }
  }
}
</script>

<template>
  <div class="login-hero">
    <div class="hero-left">
      <div class="hero-content">
        <div class="hero-logo">
          <i class="core-icon stethoscope hero-icon"></i>
        </div>
        <h1 class="hero-title">Remote Medic</h1>
        <p class="hero-subtitle">
          Plataforma médica remota con <br>
          <span class="highlight">tecnología de vanguardia</span>
        </p>
        <div class="hero-particles">
          <div class="particle p1"></div>
          <div class="particle p2"></div>
          <div class="particle p3"></div>
          <div class="particle p4"></div>
          <div class="particle p5"></div>
        </div>
      </div>
    </div>

    <div class="login-right">
      <div class="login-card">
        <div class="card-header">
          <button class="switch-btn" :class="{ active: loginFlag, idle: !loginFlag }" @click="setLogin">
            <i class="core-icon login"></i> Iniciar Sesión
          </button>
          <button class="switch-btn" :class="{ active: !loginFlag, idle: loginFlag  }" @click="setRegister">
            <i class="core-icon register-router-icon big-icon"></i> Registrarse
          </button>
        </div>

        <div class="card-body">
          <LoginView v-if="loginFlag" @register="setRegister" @error="showError" @redirect="redirectToMainPage" />
          <RegisterView v-else @login="setLogin" @error="showError" />
        </div>

        <MessageToast ref="toast" />
      </div>
    </div>
  </div>
</template>

<style scoped>
.login-hero {
  min-height: 100vh;
  display: flex;
  background: linear-gradient(135deg, #0a0e17 0%, #1a1e23 50%, #111418 100%);
  overflow: hidden;
  position: relative;
  font-family: 'Inter', sans-serif;
}

.hero-left {
  flex: 1;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(56, 170, 119, 0.2) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(16, 185, 129, 0.15) 0%, transparent 50%);
}

.hero-content {
  text-align: center;
  position: relative;
  z-index: 2;
  max-width: 500px;
  padding: 0 40px;
}

.hero-logo {
  width: 140px;
  height: 140px;
  background: linear-gradient(135deg, #38aa77 0%, #10b981 50%, #51f7ac 100%);
  border-radius: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 40px;
  box-shadow:
    0 0 60px rgba(56, 170, 119, 0.6),
    inset 0 0 40px rgba(255, 255, 255, 0.1);
  animation: logoFloat 6s ease-in-out infinite;
}

.hero-icon {
  font-size: 4rem;
  color: white;
  filter: drop-shadow(0 0 20px rgba(255, 255, 255, 0.8));
}

.hero-title {
  font-size: 3.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #fff 0%, #e2e8f0 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0 0 24px;
  letter-spacing: -0.02em;
  animation: titleGlow 3s ease-in-out infinite alternate;
}

.hero-subtitle {
  font-size: 1.3rem;
  color: #b4b6c0;
  line-height: 1.6;
  font-weight: 300;
  margin: 0 0 60px;
}

.highlight {
  background: linear-gradient(135deg, #38aa77, #51f7ac);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-weight: 600;
}

.hero-particles {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  z-index: 1;
}

.particle {
  position: absolute;
  background: rgba(56, 170, 119, 0.6);
  border-radius: 50%;
  animation: particleFloat 20s linear infinite;
}

.p1 {
  width: 12px;
  height: 12px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.p2 {
  width: 8px;
  height: 8px;
  top: 60%;
  right: 20%;
  animation-delay: 5s;
}

.p3 {
  width: 16px;
  height: 16px;
  bottom: 30%;
  left: 30%;
  animation-delay: 10s;
}

.p4 {
  width: 10px;
  height: 10px;
  top: 40%;
  right: 10%;
  animation-delay: 15s;
}

.p5 {
  width: 14px;
  height: 14px;
  bottom: 20%;
  left: 70%;
  animation-delay: 8s;
}

.login-right {
  flex: 0 0 480px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px 150px 40px 20px;
  background: linear-gradient(5deg, rgb(20 48 44 / 40%) 0%, transparent 50%);
  backdrop-filter: blur(40px);
}

.login-card {
  width: 135%;
  max-width: 467px;
  background: rgba(26, 30, 35, 0.95);
  border: 1px solid rgba(56, 170, 119, 0.4);
  border-radius: 24px;
  overflow: hidden;
  box-shadow:
    0 40px 80px rgba(0, 0, 0, 0.6),
    0 0 0 1px rgba(56, 170, 119, 0.2);
  animation: cardSlideRight 1s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

.card-header {
  display: flex;
  gap: 8px;
}

.switch-btn {
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
  i {
    background-color: #9ca3af;
  }
}

.switch-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #38aa77, #10b981);
  transition: left 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: -1;
}

.switch-btn:hover {
  color: #d1d5db;
}

.switch-btn.active::before {
  left: 0;
}

.switch-btn.active {
  background: linear-gradient(135deg, #38aa77 0%, #10b981 50%, #51f7ac 100%);
  color: white;
  box-shadow: 0 12px 35px rgba(56, 170, 119, 0.45);
  i{
    background-color: white;
  }
}

.switch-btn.idle {
  background: rgba(17, 20, 24, 0.7);
  color: #e2e8f0;
  border: 2px solid rgba(56, 170, 119, 0.4);
    i{
    background-color: #e2e8f0;
  }
}

.card-body {
  min-height: 360px;
  display: flex;
  align-items: center;
  flex-direction: column;
}

/* ANIMACIONES ESPECTACULARES */
@keyframes logoFloat {

  0%,
  100% {
    transform: translateY(0) rotate(0deg);
  }

  50% {
    transform: translateY(-20px) rotate(5deg);
  }
}

@keyframes titleGlow {
  from {
    filter: drop-shadow(0 0 20px rgba(56, 170, 119, 0.5));
    transform: scale(1);
  }

  to {
    filter: drop-shadow(0 0 40px rgba(56, 170, 119, 0.8));
    transform: scale(1.02);
  }
}

@keyframes particleFloat {
  0% {
    transform: translateY(0) rotate(0deg);
    opacity: 0;
  }

  10% {
    opacity: 1;
  }

  90% {
    opacity: 1;
  }

  100% {
    transform: translateY(-120vh) rotate(360deg);
    opacity: 0;
  }
}

@keyframes cardSlideRight {
  from {
    opacity: 0;
    transform: translateX(100px) scale(0.9);
  }

  to {
    opacity: 1;
    transform: translateX(0) scale(1);
  }
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .login-hero {
    flex-direction: column;
  }

  .login-right {
    flex: none;
    padding: 20px;
  }

  .hero-left {
    min-height: 50vh;
    padding: 60px 20px;
  }
}

@media (max-width: 480px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .card-body {
    padding: 24px 20px;
  }

  .login-card {
    margin: 0 10px;
  }
}
</style>
