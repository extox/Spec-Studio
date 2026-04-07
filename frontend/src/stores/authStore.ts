import { create } from "zustand";
import api from "@/lib/api";
import type { User, TokenResponse } from "@/types";

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (email: string, password: string) => Promise<void>;
  register: (email: string, password: string, displayName: string) => Promise<void>;
  logout: () => void;
  fetchUser: () => Promise<void>;
  initialize: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,

  login: async (email, password) => {
    const res = await api.post<TokenResponse>("/auth/login", { email, password });
    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("refresh_token", res.data.refresh_token);
    const userRes = await api.get<User>("/users/me");
    set({ user: userRes.data, isAuthenticated: true });
  },

  register: async (email, password, displayName) => {
    const res = await api.post<TokenResponse>("/auth/register", {
      email,
      password,
      display_name: displayName,
    });
    localStorage.setItem("access_token", res.data.access_token);
    localStorage.setItem("refresh_token", res.data.refresh_token);
    const userRes = await api.get<User>("/users/me");
    set({ user: userRes.data, isAuthenticated: true });
  },

  logout: () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    set({ user: null, isAuthenticated: false });
  },

  fetchUser: async () => {
    try {
      const res = await api.get<User>("/users/me");
      set({ user: res.data, isAuthenticated: true });
    } catch {
      set({ user: null, isAuthenticated: false });
    }
  },

  initialize: async () => {
    const token = localStorage.getItem("access_token");
    if (token) {
      try {
        const res = await api.get<User>("/users/me");
        set({ user: res.data, isAuthenticated: true, isLoading: false });
      } catch {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        set({ user: null, isAuthenticated: false, isLoading: false });
      }
    } else {
      set({ isLoading: false });
    }
  },
}));
