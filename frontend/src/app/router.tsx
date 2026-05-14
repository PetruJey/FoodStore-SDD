import { Suspense, lazy } from 'react';
import { createBrowserRouter, Outlet } from 'react-router-dom';

const Home = lazy(() => import('@/pages/home'));
const Productos = lazy(() => import('@/pages/productos'));
const Carrito = lazy(() => import('@/pages/carrito'));
const Checkout = lazy(() => import('@/pages/checkout'));
const Login = lazy(() => import('@/pages/login'));
const Register = lazy(() => import('@/pages/register'));
const AdminDashboard = lazy(() => import('@/pages/admin-dashboard'));
const Profile = lazy(() => import('@/pages/profile'));

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
