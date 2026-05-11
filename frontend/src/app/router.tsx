import { Suspense, lazy } from 'react';
import { createBrowserRouter, Outlet } from 'react-router-dom';

const Home = lazy(() => import('@/pages/Home'));
const Productos = lazy(() => import('@/pages/Productos'));
const Carrito = lazy(() => import('@/pages/Carrito'));
const Checkout = lazy(() => import('@/pages/Checkout'));
const Login = lazy(() => import('@/pages/Login'));
const Register = lazy(() => import('@/pages/Register'));
const AdminDashboard = lazy(() => import('@/pages/AdminDashboard'));
const Profile = lazy(() => import('@/pages/Profile'));

function Layout() {
  return (
    <Suspense
      fallback={
        <div className="flex h-screen items-center justify-center">
          <p className="text-lg text-gray-500">Cargando...</p>
        </div>
      }
    >
      <Outlet />
    </Suspense>
  );
}

export const router = createBrowserRouter([
  {
    element: <Layout />,
    children: [
      { path: '/', element: <Home /> },
      { path: '/productos', element: <Productos /> },
      { path: '/carrito', element: <Carrito /> },
      { path: '/checkout', element: <Checkout /> },
      { path: '/login', element: <Login /> },
      { path: '/registro', element: <Register /> },
      { path: '/admin', element: <AdminDashboard /> },
      { path: '/perfil', element: <Profile /> },
    ],
  },
]);
