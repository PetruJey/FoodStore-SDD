export interface User {
  id: number;
  nombre: string;
  email: string;
  roles: string[];
}

export interface CartItem {
  productoId: number;
  nombre: string;
  precio: number;
  cantidad: number;
  imagenUrl?: string;
  personalizacion?: string;
}

export interface Toast {
  id: string;
  type: 'success' | 'error' | 'info' | 'warning';
  message: string;
  duration?: number;
}

export type PaymentStatus = 'pending' | 'approved' | 'rejected' | 'in_process';

export type CheckoutStep = 'idle' | 'review' | 'payment' | 'confirming' | 'completed' | 'error';

export type Theme = 'light' | 'dark';
