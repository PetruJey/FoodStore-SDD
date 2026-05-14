import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { Theme, Toast } from '@shared/types';

interface UiState {
  theme: Theme;
  sidebarOpen: boolean;
  toasts: Toast[];
}

interface UiActions {
  toggleTheme: () => void;
  setSidebarOpen: (open: boolean) => void;
  addToast: (toast: Omit<Toast, 'id'>) => void;
  removeToast: (id: string) => void;
}

type UiStore = UiState & UiActions;

export const useUiStore = create<UiStore>()(
  persist(
    (set, get) => ({
      theme: 'light',
      sidebarOpen: false,
      toasts: [],

      toggleTheme: () =>
        set((state) => ({
          theme: state.theme === 'light' ? 'dark' : 'light',
        })),

      setSidebarOpen: (open) => set({ sidebarOpen: open }),

      addToast: (toast) => {
        const id = crypto.randomUUID();
        const newToast: Toast = { ...toast, id };
        set((state) => ({ toasts: [...state.toasts, newToast] }));
        const duration = toast.duration ?? 5000;
        setTimeout(() => {
          const current = get().toasts;
          if (current.some((t) => t.id === id)) {
            set((state) => ({
              toasts: state.toasts.filter((t) => t.id !== id),
            }));
          }
        }, duration);
      },

      removeToast: (id) =>
        set((state) => ({
          toasts: state.toasts.filter((t) => t.id !== id),
        })),
    }),
    {
      name: 'food-store-ui',
      partialize: (state) => ({ theme: state.theme }),
    },
  ),
);
