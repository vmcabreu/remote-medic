<template>
  <LoginLayout />
</template>

<script>
import LoginLayout from './components/layout/login/LoginLayout.vue';

export default {
  name: 'App',
  components: {
    LoginLayout
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  height: 100%;

}
</style>
