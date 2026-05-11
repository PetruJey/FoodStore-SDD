import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface CartItem {
  productoId: number;
  nombre: string;
  precio: number;
  cantidad: number;
  imagen?: string;
}

interface CartState {
  items: CartItem[];
  addItem: (item: CartItem) => void;
  removeItem: (productoId: number) => void;
  updateQuantity: (productoId: number, cantidad: number) => void;
  clearCart: () => void;
  totalItems: () => number;
  totalPrice: () => number;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      addItem: (item) =>
        set((state) => {
          const existing = state.items.find((i) => i.productoId === item.productoId);
          if (existing) {
            return {
              items: state.items.map((i) =>
                i.productoId === item.productoId
                  ? { ...i, cantidad: i.cantidad + item.cantidad }
                  : i,
              ),
            };
          }
          return { items: [...state.items, item] };
        }),

      removeItem: (productoId) =>
        set((state) => ({
          items: state.items.filter((i) => i.productoId !== productoId),
        })),

      updateQuantity: (productoId, cantidad) =>
        set((state) => ({
          items: state.items.map((i) =>
            i.productoId === productoId ? { ...i, cantidad: Math.max(0, cantidad) } : i,
          ),
        })),

      clearCart: () => set({ items: [] }),

      totalItems: () => get().items.reduce((sum, i) => sum + i.cantidad, 0),

      totalPrice: () => get().items.reduce((sum, i) => sum + i.precio * i.cantidad, 0),
    }),
    {
      name: 'food-store-cart',
    },
  ),
);
