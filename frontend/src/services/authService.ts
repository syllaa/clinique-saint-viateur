import axios from "axios";

import { API_BASE_URL, api } from "@/services/api";

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface CurrentUser {
  id: number;
  username: string;
  role: string;
}

export const authService = {
  login(username: string, password: string) {
    return api.post<TokenResponse>("/auth/login", { username, password }).then((r) => r.data);
  },
  /** Uses the bare axios instance on purpose: going through `api` would re-enter
   * its 401 interceptor and could loop if the refresh token itself is rejected. */
  refresh(refreshToken: string) {
    return axios
      .post<TokenResponse>(`${API_BASE_URL}/auth/refresh`, { refresh_token: refreshToken })
      .then((r) => r.data);
  },
  /** 204 on success; 400 wrong current password, 422 weak password, 429 too many tries. */
  changePassword(currentPassword: string, newPassword: string) {
    return api
      .post("/auth/change-password", { current_password: currentPassword, new_password: newPassword })
      .then(() => undefined);
  },
  me() {
    return api.get<CurrentUser>("/auth/me").then((r) => r.data);
  },
};
