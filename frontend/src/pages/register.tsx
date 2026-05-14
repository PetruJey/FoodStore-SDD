import { useNavigate } from 'react-router-dom';
import { RegisterForm } from '@/features/auth/components/RegisterForm';

export default function Register() {
  const navigate = useNavigate();

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50">
      <div className="w-full max-w-md space-y-6 rounded-lg bg-white p-8 shadow-md">
        <h1 className="text-center text-2xl font-bold text-gray-900">Crear cuenta</h1>
        <RegisterForm onSuccess={() => navigate('/')} />
        <p className="text-center text-sm text-gray-600">
          ¿Ya tenés cuenta?{' '}
          <a href="/login" className="text-blue-600 hover:text-blue-500">
            Iniciá sesión
          </a>
        </p>
      </div>
    </div>
  );
}
