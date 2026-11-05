import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { authService, type CurrentUser } from "@/services/authService";

const STORAGE_KEY = "sv_auth";

export const useAuthStore = defineStore("auth", () => {
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const user = ref<CurrentUser | null>(null);

  const isAuthenticated = computed(() => !!accessToken.value);
  const isAdmin = computed(() => user.value?.role === "admin");

  function persist() {
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({ accessToken: accessToken.value, refreshToken: refreshToken.value, user: user.value }),
    );
  }

  function restoreSession() {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return;
    try {
      const data = JSON.parse(raw);
      accessToken.value = data.accessToken ?? null;
      refreshToken.value = data.refreshToken ?? null;
      user.value = data.user ?? null;
    } catch {
      localStorage.removeItem(STORAGE_KEY);
    }
  }

  async function login(username: string, password: string) {
    const tokens = await authService.login(username, password);
    accessToken.value = tokens.access_token;
    refreshToken.value = tokens.refresh_token;
    user.value = await authService.me();
    persist();
  }

  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    localStorage.removeItem(STORAGE_KEY);
  }

  return { accessToken, refreshToken, user, isAuthenticated, isAdmin, restoreSession, login, logout };
});
