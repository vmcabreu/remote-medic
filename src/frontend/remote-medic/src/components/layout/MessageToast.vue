<script>
import { ref } from 'vue'
import '@/assets/styles/icons.css'


export default {
  name: 'MessageToast',
  components: {},
  setup() {
    const visible = ref(false)
    const message = ref('')

    const show = (msg, duration = 2000) => {
      message.value = msg
      visible.value = true
      setTimeout(() => visible.value = false, duration)
    }

    return { visible, message, show }
  }
}
</script>

<template>
  <transition name="fade">
    <div v-if="visible" class="toast">
      <i class="core-icon error-octogonal icon-white"></i>
      <span>{{ message }}</span>
    </div>
  </transition>
</template>

<style scoped>
.toast {
  position: fixed;
  top: 20px;
  right: 20px;
  background: #f56565;
  color: white;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 20px;
  border-radius: 6px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  z-index: 9999;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.fade-enter-to,
.fade-leave-from {
  opacity: 1;
}

.icon-white {
  width: 25px !important;
  height: 25px !important;
  background-color: white !important;
}
</style>
