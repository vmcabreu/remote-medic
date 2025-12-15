<script>
import { ref } from "vue";
import MessageToast from "./../MessageToast.vue";
import { useAuthStore } from "@/stores/auth.store";

export default {
  name: "MainLayout",

  components: {
    MessageToast,
  },

  setup() {
    const authStore = useAuthStore()
    const toast = ref(null);

    const showError = (msg) => {
      toast.value?.show(msg);
    };

    const logout = () => {
      authStore.logout()
    };

    return {
      toast,
      showError,
      logout,
    };
  },
};
</script>

<template>
  <div class="layout">
    <MessageToast ref="toast" />

    <aside class="sidebar">
      <img
        src="@/assets/images/remote-medic-logo.png"
        alt="Remote Medic Logo"
        class="sidebar-image"
      />

      <nav class="menu">
        <router-link to="/" class="menu-item" exact-active-class="active">
          <i class="core-icon dashboard-monitor small-icon"></i>
          <span>Dashboard</span>
        </router-link>
        <router-link to="/patients" class="menu-item">
          <i class="core-icon user-group small-icon"></i>
          <span>Pacientes</span>
        </router-link>
        <router-link to="/medicines" class="menu-item">
          <i class="core-icon medication small-icon"></i>
          <span>Medicinas</span>
        </router-link>
      </nav>
    </aside>

    <div class="main">
      <header class="header">
        <div class="header-button-bar">
          <router-link to="/profile" class="logout-button">
            <i class="core-icon circle-user small-icon"></i>
            <span>Perfil</span>
          </router-link>
          <button class="logout-button" @click="logout">
            <i class="core-icon logout small-icon"></i>
            <span>Cerrar sesión</span>
          </button>
        </div>
      </header>

      <section class="content">
        <router-view />
      </section>
    </div>
  </div>
</template>

<style scoped>
.sidebar-image {
  padding-bottom: 30px;
}

.header-button-bar {
  display: flex;
  gap: 10px;
  align-items: end;
  justify-content: center;
}

/* Layout general */
.layout {
  display: flex;
  height: 100vh;
  background: #1a1e23;
  color: #fff;
  font-family: Inter, sans-serif;
}

/* Sidebar */
.sidebar {
  width: 240px;
  background: #111418;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.logo {
  font-size: 20px;
  margin-bottom: 30px;
  text-align: center;
}

.menu {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.menu-item {
  padding: 12px;
  border-radius: 6px;
  text-decoration: none;
  color: #cfd3dc;
  display: flex;
  justify-content: center;
  gap: 10px;
  align-items: flex-end;
  transition: 0.25s;

  i {
    background-color: #38aa77;
  }

  &:hover {
    background: #1f252d;

    i {
      background-color: #45d494;
    }
  }

  &.active {
    background: #38aa77;
    color: #fff;

    i {
      background-color: #1a1e23;
    }
  }
}

/* Main */
.main {
  flex: 1;
  display: flex;
  flex-direction: column;
}

/* Header */
.header {
  height: 60px;
  background: #111418;
  display: flex;
  align-items: center;
  justify-content: flex-end;
  padding: 0 20px;
  border-bottom: 1px solid #222;
}

.title {
  font-size: 18px;
}

.logout-button {
  background: transparent;
  text-decoration: none;
  border: 1px solid #38aa77;
  color: #38aa77;
  padding: 6px 12px;
  border-radius: 4px;
  cursor: pointer;
  transition: 0.25s;
  display: flex;
  justify-content: center;
  align-items: end;
  gap: 15px;

  i {
    background-color: #38aa77;
  }

  &:hover {
    background: #51f7ac;
    color: white;

    i {
      background-color: #111418;
    }
  }
}

/* Content */
.content {
  flex: 1;
  padding: 20px;
  overflow-y: auto;
}
</style>
