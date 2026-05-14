import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { CartItem } from '@shared/types';

interface CartState {
  items: CartItem[];
  lastUpdated: number | null;
}

interface CartActions {
  addItem: (item: CartItem) => void;
  removeItem: (productoId: number) => void;
  updateQuantity: (productoId: number, cantidad: number) => void;
  clearCart: () => void;
  totalItems: () => number;
  totalPrice: () => number;
  getItem: (productoId: number) => CartItem | undefined;
}

type CartStore = CartState & CartActions;

export const useCartStore = create<CartStore>()(
  persist(
    (set, get) => ({
      items: [],
      lastUpdated: null,

      addItem: (item) =>
        set((state) => {
          const existing = state.items.find(
            (i) => i.productoId === item.productoId && i.personalizacion === item.personalizacion,
          );
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.productoId === item.productoId && i.personalizacion === item.personalizacion
                  ? { ...i, cantidad: i.cantidad + item.cantidad }
                  : i,
              ),
              lastUpdated: Date.now(),
            };
          }
          return { items: [...state.items, item], lastUpdated: Date.now() };
        }),

      removeItem: (productoId) =>
        set((state) => ({
          items: state.items.filter((i) => i.productoId !== productoId),
          lastUpdated: Date.now(),
        })),

      updateQuantity: (productoId, cantidad) =>
        set((state) => ({
          items: state.items.map((i) =>
            i.productoId === productoId ? { ...i, cantidad } : i,
          ),
          lastUpdated: Date.now(),
        })),

      clearCart: () => set({ items: [], lastUpdated: Date.now() }),

      totalItems: () => get().items.reduce((sum, i) => sum + i.cantidad, 0),

      totalPrice: () =>
        get().items.reduce((sum, i) => sum + i.precio * i.cantidad, 0),

      getItem: (productoId) => get().items.find((i) => i.productoId === productoId),
    }),
    {
      name: 'food-store-cart',
      partialize: (state) => ({
        items: state.items,
        lastUpdated: state.lastUpdated,
      }),
    },
  ),
);
