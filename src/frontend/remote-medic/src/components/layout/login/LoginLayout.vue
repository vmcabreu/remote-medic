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
    const showError = (msg) => {
      toast.value.show(msg)
    }
    function setRegister() {
      loginFlag.value = false
    }
    function setLogin() {
      loginFlag.value = true
    }
    function redirectToMainPage() {
      router.push({ name: 'Home' })
    }
    return { router,loginFlag, setRegister, setLogin, toast, showError ,redirectToMainPage}
  }
}
</script>

<template>
  <div class="main-container">
    <div class="login-card">
      <LoginView v-if="loginFlag === true" @register="setRegister" @error="showError"
        @redirect="redirectToMainPage()" />
      <RegisterView v-if="loginFlag === false" @login="setLogin" @error="showError" />
      <MessageToast ref="toast" />
    </div>
    <div class="bubbles">
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
      <div class="bubble"></div>
    </div>
  </div>

</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main-container {
  background: #1a1e23;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

.bubbles {
  position: relative;
  width: 100%;
  height: 100vh;
  overflow: hidden;
}

.bubble {
  position: absolute;
  left: var(--bubble-left-offset);
  bottom: -75%;
  display: block;
  width: var(--bubble-radius);
  height: var(--bubble-radius);
  border-radius: 50%;
  animation: float-up var(--bubble-float-duration) var(--bubble-float-delay) ease-in infinite;
}

.bubble::before {
  position: absolute;
  content: '';
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: hsla(183, 94%, 76%, 0.3);
  border-radius: inherit;
  animation: var(--bubble-sway-type) var(--bubble-sway-duration) var(--bubble-sway-delay) ease-in-out alternate infinite;
}

/* Variables CSS personalizadas para cada burbuja */
.bubble:nth-child(1) {
  --bubble-left-offset: 15vw;
  --bubble-radius: 3vw;
  --bubble-float-duration: 8s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 1s;
  --bubble-sway-delay: 2s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(2) {
  --bubble-left-offset: 85vw;
  --bubble-radius: 7vw;
  --bubble-float-duration: 11s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 3s;
  --bubble-sway-delay: 1s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(3) {
  --bubble-left-offset: 45vw;
  --bubble-radius: 2vw;
  --bubble-float-duration: 9s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 0s;
  --bubble-sway-delay: 3s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(4) {
  --bubble-left-offset: 70vw;
  --bubble-radius: 5vw;
  --bubble-float-duration: 7s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 2s;
  --bubble-sway-delay: 0s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(5) {
  --bubble-left-offset: 25vw;
  --bubble-radius: 8vw;
  --bubble-float-duration: 12s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 4s;
  --bubble-sway-delay: 2s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(6) {
  --bubble-left-offset: 90vw;
  --bubble-radius: 4vw;
  --bubble-float-duration: 10s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 1s;
  --bubble-sway-delay: 4s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(7) {
  --bubble-left-offset: 10vw;
  --bubble-radius: 6vw;
  --bubble-float-duration: 8s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 3s;
  --bubble-sway-delay: 1s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(8) {
  --bubble-left-offset: 60vw;
  --bubble-radius: 3vw;
  --bubble-float-duration: 9s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 0s;
  --bubble-sway-delay: 3s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(9) {
  --bubble-left-offset: 35vw;
  --bubble-radius: 9vw;
  --bubble-float-duration: 11s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 2s;
  --bubble-sway-delay: 0s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(10) {
  --bubble-left-offset: 80vw;
  --bubble-radius: 2vw;
  --bubble-float-duration: 7s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 4s;
  --bubble-sway-delay: 2s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(11) {
  --bubble-left-offset: 5vw;
  --bubble-radius: 5vw;
  --bubble-float-duration: 10s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 1s;
  --bubble-sway-delay: 4s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(12) {
  --bubble-left-offset: 95vw;
  --bubble-radius: 7vw;
  --bubble-float-duration: 8s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 3s;
  --bubble-sway-delay: 1s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(13) {
  --bubble-left-offset: 50vw;
  --bubble-radius: 4vw;
  --bubble-float-duration: 12s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 0s;
  --bubble-sway-delay: 3s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(14) {
  --bubble-left-offset: 20vw;
  --bubble-radius: 8vw;
  --bubble-float-duration: 9s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 2s;
  --bubble-sway-delay: 0s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(15) {
  --bubble-left-offset: 75vw;
  --bubble-radius: 3vw;
  --bubble-float-duration: 11s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 4s;
  --bubble-sway-delay: 2s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(16) {
  --bubble-left-offset: 40vw;
  --bubble-radius: 6vw;
  --bubble-float-duration: 7s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 1s;
  --bubble-sway-delay: 4s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(17) {
  --bubble-left-offset: 65vw;
  --bubble-radius: 9vw;
  --bubble-float-duration: 10s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 3s;
  --bubble-sway-delay: 1s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(18) {
  --bubble-left-offset: 30vw;
  --bubble-radius: 2vw;
  --bubble-float-duration: 8s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 0s;
  --bubble-sway-delay: 3s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(19) {
  --bubble-left-offset: 85vw;
  --bubble-radius: 5vw;
  --bubble-float-duration: 12s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 2s;
  --bubble-sway-delay: 0s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(20) {
  --bubble-left-offset: 12vw;
  --bubble-radius: 7vw;
  --bubble-float-duration: 9s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 4s;
  --bubble-sway-delay: 2s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(21) {
  --bubble-left-offset: 55vw;
  --bubble-radius: 4vw;
  --bubble-float-duration: 11s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 1s;
  --bubble-sway-delay: 4s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(22) {
  --bubble-left-offset: 78vw;
  --bubble-radius: 8vw;
  --bubble-float-duration: 7s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 3s;
  --bubble-sway-delay: 1s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(23) {
  --bubble-left-offset: 25vw;
  --bubble-radius: 3vw;
  --bubble-float-duration: 10s;
  --bubble-sway-duration: 4s;
  --bubble-float-delay: 0s;
  --bubble-sway-delay: 3s;
  --bubble-sway-type: sway-left-to-right;
}

.bubble:nth-child(24) {
  --bubble-left-offset: 92vw;
  --bubble-radius: 6vw;
  --bubble-float-duration: 8s;
  --bubble-sway-duration: 5s;
  --bubble-float-delay: 2s;
  --bubble-sway-delay: 0s;
  --bubble-sway-type: sway-right-to-left;
}

.bubble:nth-child(25) {
  --bubble-left-offset: 48vw;
  --bubble-radius: 9vw;
  --bubble-float-duration: 12s;
  --bubble-sway-duration: 6s;
  --bubble-float-delay: 4s;
  --bubble-sway-delay: 2s;
  --bubble-sway-type: sway-left-to-right;
}

/* Keyframes para las animaciones */
@keyframes float-up {
  to {
    transform: translateY(-175vh);
  }
}

@keyframes sway-left-to-right {
  from {
    transform: translateX(-100%);
  }

  to {
    transform: translateX(100%);
  }
}

@keyframes sway-right-to-left {
  from {
    transform: translateX(100%);
  }

  to {
    transform: translateX(-100%);
  }
}
</style>
