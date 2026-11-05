import { api } from "@/services/api";

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
  me() {
    return api.get<CurrentUser>("/auth/me").then((r) => r.data);
  },
};
