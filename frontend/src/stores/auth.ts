import { defineStore } from "pinia";
import { computed, ref } from "vue";

import { authService, type CurrentUser, type TokenResponse } from "@/services/authService";
import { storageGet, storageRemove, storageSet } from "@/utils/storage";

const STORAGE_KEY = "sv_auth";

export const useAuthStore = defineStore("auth", () => {
  const accessToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const user = ref<CurrentUser | null>(null);
  // Set at login when the password typed is the documented default or too
  // short: the admin dashboard then asks to change it. Session-only.
  const weakPassword = ref(false);

  const isAuthenticated = computed(() => !!accessToken.value);
  const isAdmin = computed(() => user.value?.role === "admin");

  function persist() {
    storageSet(
      STORAGE_KEY,
      JSON.stringify({ accessToken: accessToken.value, refreshToken: refreshToken.value, user: user.value }),
    );
  }

  function restoreSession() {
    const raw = storageGet(STORAGE_KEY);
    if (!raw) return;
    try {
      const data = JSON.parse(raw);
      accessToken.value = data.accessToken ?? null;
      refreshToken.value = data.refreshToken ?? null;
      user.value = data.user ?? null;
    } catch {
      storageRemove(STORAGE_KEY);
    }
  }

  /** Stores a fresh token pair (after login or a silent refresh). */
  function setTokens(tokens: TokenResponse) {
    accessToken.value = tokens.access_token;
    refreshToken.value = tokens.refresh_token;
    persist();
  }

  async function login(username: string, password: string) {
    setTokens(await authService.login(username, password));
    weakPassword.value = password === "admin123" || password.length < 10;
    user.value = await authService.me();
    persist();
  }

  function logout() {
    accessToken.value = null;
    refreshToken.value = null;
    user.value = null;
    weakPassword.value = false;
    storageRemove(STORAGE_KEY);
  }

  return {
    accessToken,
    refreshToken,
    user,
    weakPassword,
    isAuthenticated,
    isAdmin,
    restoreSession,
    setTokens,
    login,
    logout,
  };
});
