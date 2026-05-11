import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface User {
  id: number;
  email: string;
  nombre: string;
  roles: string[];
}

interface AuthState {
  user: User | null;
  token: string | null;
  refreshToken: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string, refreshToken: string) => void;
  logout: () => void;
  setUser: (user: User) => void;
  updateToken: (token: string) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      refreshToken: null,
      isAuthenticated: false,

      login: (user, token, refreshToken) => {
        localStorage.setItem('auth-token', token);
        localStorage.setItem('refresh-token', refreshToken);
        set({ user, token, refreshToken, isAuthenticated: true });
      },

      logout: () => {
        localStorage.removeItem('auth-token');
        localStorage.removeItem('refresh-token');
        set({ user: null, token: null, refreshToken: null, isAuthenticated: false });
      },

      setUser: (user) => set({ user }),

      updateToken: (token) => {
        localStorage.setItem('auth-token', token);
        set({ token });
      },
    }),
    {
      name: 'food-store-auth',
    },
  ),
);
