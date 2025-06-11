<script>
import { reactive } from "vue";

export default {
  name: 'LoginView',
  emits: ['register'],
  setup(props, { emit }) {
    const user = reactive({
      username: '',
      password: ''
    });

    const login = () => {
      console.log(user);
    }

    const changeToRegister = () => emit('register')

    return {
      user,
      login,
      changeToRegister
    };
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
    <button class="button-template button-success" @click="login()">Login</button>
    <button class="button-template button-grey" @click="changeToRegister()">Registrarse</button>
  </div>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped></style>
