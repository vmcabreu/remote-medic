import { defineStore } from "pinia";
import { ref, computed } from "vue";
import authService from "./../services/authService";
import router from "@/router";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(null);
  const isAuthenticated = computed(() => !!token.value);
  const user = ref(null);

  const getUser = async () => {
    if (!user.value) {
      try {
        const userData = await authService.getUserData();
        user.value = userData;
        return user.value;
      } catch (error) {
        console.error("Error getting user:", error);
        user.value = null;
        return null;
      }
    }
    return user.value;
  };

  const initAuth = async () => {
    const savedToken = sessionStorage.getItem("authToken");
    if (savedToken) {
      token.value = savedToken;
      await getUser();
    }
  };

  const setToken = (t) => {
    token.value = t;
    if (t) {
      sessionStorage.setItem("authToken", t);
    } else {
      sessionStorage.removeItem("authToken");
    }
  };

  const setUser = (u) => {
    user.value = u;
  };

  const logout = () => {
    token.value = null;
    user.value = null;
    sessionStorage.removeItem("authToken");
    router.push("/login");
  };

  initAuth();

  return {
    token,
    user,
    isAuthenticated,
    setToken,
    setUser,
    getUser,
    logout,
    initAuth,
  };
});
