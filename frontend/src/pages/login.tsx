import { useNavigate } from 'react-router-dom';
import { LoginForm } from '@/features/auth/components/LoginForm';

export default function Login() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-md">
        <h1 className="text-center text-2xl font-bold text-gray-900">Iniciar sesión</h1>
        <LoginForm onSuccess={() => navigate('/')} />
        <p className="text-center text-sm text-gray-600">
          ¿No tenés cuenta?{' '}
          <a href="/register" className="text-blue-600 hover:text-blue-500">
            Registrate
          </a>
        </p>
      </div>
    </div>
  );
}
