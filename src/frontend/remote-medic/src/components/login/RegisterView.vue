<script>
import { reactive } from 'vue';

export default {
  name: 'RegisterView',
  emits: ['login'],
  setup(props, { emit }) {
    const user = reactive({
      username: '',
      password: '',
      repeatPassword: '',
      email: ''
    });

    const errorsMessage = reactive({
      username: {
        errors: {
          emptyOrNull: {
            active: false,
            message: "Debe de insertar su nombre de usuario."
          }
        }
      },
      password: {
        errors: {
          emptyOrNull: {
            active: false,
            message: "Debe de insertar su contraseña."
          },
          formatValidator: {
            active: false,
            message: "Su contraseña debe contener: 1 mayúscula, 1 minúscula, 1 número y un caracter especial(*-?!)"
          }
        }
      },
      repeatPassword: {
        errors: {
          emptyOrNull: {
            active: false,
            message: "Debe de volver a insertar su contraseña."
          },
          isSame: {
            active: false,
            message: "Las contraseñas deben coincidir"
          }
        }
      },
      email: {
        errors: {
          emptyOrNull: {
            active: false,
            message: "Debe de insertar su email."
          },
          formatValidator: {
            active: false,
            message: "Su contraseña debe contener: 1 mayúscula, 1 minúscula, 1 número y un caracter especial(*-?!)"
          }
        }
      }
    });

    const checkForm = () => {
      console.log(errorsMessage)
      Object.keys(user).forEach(element => {
        switch (element) {
          case 'username':

            break;
          case 'email':

            break;
          case 'password':

            break;
          case 'repeatPassword':

            break;


          default:
            break;
        }
      });

    }

    const register = () => {
      console.log(user);
    };

    const changeToRegister = () => {
      emit('login');
    };

    return {
      user,
      register,
      changeToRegister,
      errorsMessage,
      checkForm
    };
  }
}
</script>

<template>
  <h4>Registrarse</h4>
  <form v-on:submit.prevent="register()" class="register-container">
    <div class="login-form-container">
      <div class="input-layout">
        <p>Usuario:</p>
        <input type="text" required v-model.trim="user.username">
      </div>
      <div class="input-layout">
        <p>Email:</p>
        <input type="email" required v-model.trim="user.email">
      </div>
      <div class="input-layout">
        <p>Contraseña:</p>
        <input type="password" required v-model.trim="user.password">
      </div>
      <div class="input-layout">
        <p>Repetir contraseña:</p>
        <input type="password" required v-model.trim="user.repeatPassword">
      </div>
    </div>
    <div class="flex">
      <button class="button-template button-success" type="submit">Registrarse</button>
      <button class="button-template button-grey" type="button" @click="changeToRegister()">Iniciar Sesión</button>
    </div>
  </form>
</template>


<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
.register-container {
  display: flex;
  flex-direction: column;
  gap: 10px;
  align-items: center;
}

.login-form-container {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 10px;
}
</style>
