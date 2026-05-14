import { Routes, Route, Navigate } from 'react-router-dom';

function PublicLayout({ children }: { children: React.ReactNode }) {
  return <>{children}</>;
}

function PrivateLayout({ children }: { children: React.ReactNode }) {
  // TODO: add auth guard with navigate to /login
  return <>{children}</>;
}

function Home() {
  return <h1 className="text-3xl font-bold">Food Store</h1>;
}

function LoginPage() {
  return <h1>Iniciar Sesión</h1>;
}

function RegisterPage() {
  return <h1>Registrarse</h1>;
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
