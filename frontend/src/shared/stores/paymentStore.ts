import { create } from 'zustand';
import type { CheckoutStep, PaymentStatus } from '@shared/types';

interface PaymentState {
  checkoutStep: CheckoutStep;
  pedidoId: number | null;
  preferenceId: string | null;
  paymentStatus: PaymentStatus | null;
  error: string | null;
}

interface PaymentActions {
  startCheckout: (pedidoId: number) => void;
  setPreference: (id: string) => void;
  updatePaymentStatus: (status: PaymentStatus) => void;
  setError: (error: string) => void;
  resetPayment: () => void;
}

type PaymentStore = PaymentState & PaymentActions;

const initialState: PaymentState = {
  checkoutStep: 'idle',
  pedidoId: null,
  preferenceId: null,
  paymentStatus: null,
  error: null,
};

export const usePaymentStore = create<PaymentStore>()((set) => ({
  ...initialState,

  startCheckout: (pedidoId) =>
    set({
      checkoutStep: 'review',
      pedidoId,
      preferenceId: null,
      paymentStatus: null,
      error: null,
    }),

  setPreference: (id) =>
    set({ preferenceId: id, checkoutStep: 'payment' }),

  updatePaymentStatus: (status) =>
    set({ paymentStatus: status }),

  setError: (error) =>
    set({ error, checkoutStep: 'error' }),

  resetPayment: () => set(initialState),
}));
