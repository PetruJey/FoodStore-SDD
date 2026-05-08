# 9. Gestión de Estado con Zustand

Zustand es la librería de gestión de estado global del frontend. Food Store requiere cuatro stores con responsabilidades claramente separadas.

[DIAGRAMA: Arquitectura Frontend - Feature-Sliced Design] Capas del frontend con flujo de imports de arriba hacia abajo: Pages a Features a Hook/Store a API a Types, sin cross-imports entre features. (1) Pages/pages/: solo define la ruta y delega a los features. (2) Cuatro features: feature/auth (LoginForm, RegisterForm, ProtectedRoute HOC), feature/store (CatalogoGrid, CartDrawer, CheckoutForm), feature/pedidos (PedidosList, PedidoDetail, HistorialTimeline, PaymentStatus), feature/admin (Dashboard, CRUDs, GestionPedidos, StockTable). (3) Hooks con TanStack Query: useAuth, useProductos, usePedidos, useAdmin. Stores Zustand: authStore, cartStore, paymentStore, uiStore. (4) API/Axios con interceptores JWT. (5) Types con strict:true sin any. Al pie: Components compartidos y React Router DOM.

Figura 6 — Los cuatro stores Zustand y sus responsabilidades. Persistencia selectiva por store.

| Store | Archivo | Estado que gestiona | Middleware | Persiste |
|-------|---------|---------------------|------------|----------|
| authStore | store/authStore.ts | accessToken, usuario, isAuthenticated | persist | Sí — solo el accessToken |
| cartStore | store/cartStore.ts | items del carrito, cantidades, personalizaciones | persist | Sí — items completos (v1) |
| paymentStore | store/paymentStore.ts | Estado del proceso de pago MP: status, mpPaymentId | Ninguno (sesión) | No — se resetea al recargar |
| uiStore | store/uiStore.ts | cartOpen, sidebarOpen, confirmModal activo | Ninguno | No |

**Buenas prácticas de consumo de stores:**

Suscripción por slice: `const itemCount = useCartStore(s => s.itemCount())` — evita re-renders innecesarios.

Actions extraídas sin re-render: `const { addItem } = useCartStore()`

Nunca suscribirse al store completo sin selector: ❌ `const store = useCartStore()`

Acceso fuera de React (interceptores): `useAuthStore.getState().accessToken`

authStore: partialize → solo accessToken. Al recargar, GET /api/v1/auth/me reconstruye usuario.
