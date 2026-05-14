import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import apiClient from '@/shared/api/client';
import type { User, LoginRequest, RegisterRequest, TokenResponse } from '@/features/auth/types';

export type { User };

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  login: (data: LoginRequest) => Promise<void>;
  register: (data: RegisterRequest) => Promise<void>;
  logout: () => Promise<void>;
  refresh: () => Promise<void>;
  clearError: () => void;
}

function extractError(err: unknown): string {
  if (err && typeof err === 'object') {
    const axiosErr = err as { response?: { data?: { detail?: string } } };
    if (axiosErr.response?.data?.detail) {
      return axiosErr.response.data.detail;
    }
  }
  if (err instanceof Error) return err.message;
  return 'Error inesperado';
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,
      isLoading: false,
      error: null,

      login: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const { data: res } = await apiClient.post<TokenResponse>('/auth/login', data);
          set({
            user: res.user,
            token: res.access_token,
            refreshToken: res.refresh_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (err) {
          set({ isLoading: false, error: extractError(err) });
          throw err;
        }
      },

      register: async (data) => {
        set({ isLoading: true, error: null });
        try {
          const { data: res } = await apiClient.post<TokenResponse>('/auth/register', data);
          set({
            user: res.user,
            token: res.access_token,
            refreshToken: res.refresh_token,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (err) {
          set({ isLoading: false, error: extractError(err) });
          throw err;
        }
      },

      logout: async () => {
        const { refreshToken } = get();
        try {
          if (refreshToken) {
            await apiClient.post('/auth/logout', { refresh_token: refreshToken });
          }
        } catch {
          // ignore logout errors
        } finally {
          set({
            user: null,
            token: null,
            refreshToken: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      },

      refresh: async () => {
        const storedRefresh = get().refreshToken;
        if (!storedRefresh) {
          set({ user: null, token: null, refreshToken: null, isAuthenticated: false });
          return;
        }
        try {
          const { data: res } = await apiClient.post<TokenResponse>('/auth/refresh', {
            refresh_token: storedRefresh,
          });
          set({
            token: res.access_token,
            refreshToken: res.refresh_token ?? storedRefresh,
            isAuthenticated: true,
          });
        } catch {
          set({ user: null, token: null, refreshToken: null, isAuthenticated: false });
        }
      },

      clearError: () => set({ error: null }),
    }),
    {
      name: 'food-store-auth',
      partialize: (state) => ({
        user: state.user,
        token: state.token,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    },
  ),
);
