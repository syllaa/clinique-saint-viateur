import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios";

import { useAuthStore } from "@/stores/auth";

// 127.0.0.1, not "localhost": see the proxy note in vite.config.ts.
export const API_BASE_URL: string = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE_URL,
});

/** Resolves a backend-relative media path (e.g. "/uploads/images/x.jpg") to a full URL. */
export function mediaUrl(path: string | null | undefined): string | null {
  if (!path) return null;
  if (path.startsWith("http://") || path.startsWith("https://")) return path;
  return `${API_BASE_URL}${path}`;
}

api.interceptors.request.use((config) => {
  const auth = useAuthStore();
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
});

// One refresh at a time: concurrent 401s (e.g. the admin dashboard loading
// several lists at once) all wait on the same request instead of each one
// spending the refresh token.
let refreshing: Promise<string | null> | null = null;

async function refreshAccessToken(): Promise<string | null> {
  const auth = useAuthStore();
  if (!auth.refreshToken) return null;
  try {
    // Imported lazily: authService imports this module, so a static import would be circular.
    const { authService } = await import("@/services/authService");
    const tokens = await authService.refresh(auth.refreshToken);
    auth.setTokens(tokens);
    return tokens.access_token;
  } catch {
    return null;
  }
}

type RetriableConfig = InternalAxiosRequestConfig & { _retried?: boolean };

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const original = error.config as RetriableConfig | undefined;
    const isAuthCall = original?.url?.startsWith("/auth/login") || original?.url?.startsWith("/auth/refresh");

    if (error.response?.status === 401 && original && !original._retried && !isAuthCall) {
      original._retried = true;
      refreshing ??= refreshAccessToken().finally(() => {
        refreshing = null;
      });
      const newToken = await refreshing;
      if (newToken) {
        original.headers.Authorization = `Bearer ${newToken}`;
        return api(original);
      }
    }

    if (error.response?.status === 401) {
      useAuthStore().logout();
    }
    return Promise.reject(error);
  },
);
