import { Routes, Route, Navigate, Link, useNavigate } from 'react-router-dom';
import { useAuthStore } from '@shared/stores/authStore';
import api from '@shared/api/axios';
import LoginPage from './pages/Login';
import RegisterPage from './pages/Register';

function Navbar() {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);
  const user = useAuthStore((s) => s.user);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const refreshToken = useAuthStore.getState().refreshToken;
      if (refreshToken) {
        await api.post('/auth/logout', { refresh_token: refreshToken });
      }
    } catch {
      // si el logout remoto falla, igual limpiamos local
    }

    useAuthStore.getState().logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-sm">
      <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="flex h-16 items-center justify-between">
          <Link to="/" className="text-xl font-bold text-gray-900">
            Food Store
          </Link>

          <div className="flex items-center gap-4">
            {isAuthenticated ? (
              <>
                <Link
                  to="/perfil"
                  className="text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  {user?.nombre}
                </Link>
                <button
                  onClick={handleLogout}
                  className="rounded-md bg-gray-100 px-3 py-1.5 text-sm font-medium text-gray-700 hover:bg-gray-200"
                >
                  Cerrar sesión
                </button>
              </>
            ) : (
              <>
                <Link
                  to="/login"
                  className="text-sm font-medium text-gray-700 hover:text-gray-900"
                >
                  Iniciar sesión
                </Link>
                <Link
                  to="/register"
                  className="rounded-md bg-indigo-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-indigo-700"
                >
                  Registrarse
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}

function PublicLayout({ children }: { children: React.ReactNode }) {
  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
    </>
  );
}

function PrivateLayout({ children }: { children: React.ReactNode }) {
  const isAuthenticated = useAuthStore((s) => s.isAuthenticated);

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  return (
    <>
      <Navbar />
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">{children}</main>
    </>
  );
}

function Home() {
  return <h1 className="text-3xl font-bold">Food Store</h1>;
}

function ProductosPage() {
  return <h1>Productos</h1>;
}

function ProductoDetailPage() {
  return <h1>Producto</h1>;
}

export default function App() {
  return (
    <Routes>
      <Route element={<PublicLayout><Home /></PublicLayout>} path="/" />
      <Route element={<PublicLayout><LoginPage /></PublicLayout>} path="/login" />
      <Route element={<PublicLayout><RegisterPage /></PublicLayout>} path="/register" />
      <Route element={<PublicLayout><ProductosPage /></PublicLayout>} path="/productos" />
      <Route element={<PublicLayout><ProductoDetailPage /></PublicLayout>} path="/productos/:id" />
      <Route element={<PrivateLayout><></></PrivateLayout>} path="/dashboard/*" />
      <Route element={<Navigate to="/" replace />} path="*" />
    </Routes>
  );
}
