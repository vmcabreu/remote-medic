<script>
import { ref } from 'vue'
import LoginView from './../../login/LoginView.vue'
import RegisterView from './../../login/RegisterView.vue'

export default {
  name: 'LoginLayout',
  components: {
    LoginView,
    RegisterView
  },
  setup() {
    const loginFlag = ref(true)
    function setRegister() {
      loginFlag.value = false
    }
    function setLogin() {
      loginFlag.value = true
    }
    return {
      loginFlag,
      setRegister,
      setLogin
    };
  }
}
</script>

<template>
  <div class="main-container">
    <div class="login-card">
      <LoginView v-if="loginFlag === true" @register="setRegister" />
      <RegisterView v-if="loginFlag === false" @login="setLogin" />
    </div>
  </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.main-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
}

</style>
