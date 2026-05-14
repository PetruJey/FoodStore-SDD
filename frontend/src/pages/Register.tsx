import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { isAxiosError } from 'axios';
import api from '@shared/api/axios';
import { useAuthStore } from '@shared/stores/authStore';

interface FieldErrors {
  nombre?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
}

const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export default function RegisterPage() {
  const [nombre, setNombre] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [fieldErrors, setFieldErrors] = useState<FieldErrors>({});
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const login = useAuthStore((s) => s.login);

  const validate = (): boolean => {
    const errors: FieldErrors = {};

    if (nombre.trim().length < 2) {
      errors.nombre = 'El nombre debe tener al menos 2 caracteres';
    }

    if (!EMAIL_REGEX.test(email.trim())) {
      errors.email = 'Ingresá un email válido';
    }

    if (password.length < 8) {
      errors.password = 'La contraseña debe tener al menos 8 caracteres';
    }

    if (password !== confirmPassword) {
      errors.confirmPassword = 'Las contraseñas no coinciden';
    }

    setFieldErrors(errors);
    return Object.keys(errors).length === 0;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setFieldErrors({});

    if (!validate()) return;

    setLoading(true);

    try {
      const { data } = await api.post('/auth/register', {
        nombre: nombre.trim(),
        email: email.trim(),
        password,
      });

      login(
        { accessToken: data.access_token, refreshToken: data.refresh_token },
        data.user,
      );

      navigate('/');
    } catch (err: unknown) {
      if (isAxiosError(err)) {
        const status = err.response?.status;
        const detail = err.response?.data?.detail;

        if (status === 409) {
          setError('Este email ya está registrado');
        } else if (status === 422 && detail) {
          if (Array.isArray(detail)) {
            const backendErrors: FieldErrors = {};
            for (const validationErr of detail) {
              const loc = (validationErr as { loc?: string[] })?.loc;
              const msg = (validationErr as { msg?: string })?.msg;
              const field = loc?.[loc.length - 1];
              if (field && ['nombre', 'email', 'password'].includes(field)) {
                backendErrors[field as keyof FieldErrors] = msg || 'Error de validación';
              }
            }
            if (Object.keys(backendErrors).length > 0) {
              setFieldErrors(backendErrors);
            } else {
              setError('Error de validación');
            }
          } else {
            setError(String(detail));
          }
        } else {
          setError('Ocurrió un error. Intentalo de nuevo.');
        }
      } else {
        setError('Ocurrió un error. Intentalo de nuevo.');
      }
    } finally {
      setLoading(false);
    }
  };

  const inputClass = (field: keyof FieldErrors) =>
    `mt-1 block w-full rounded-md border px-3 py-2 shadow-sm focus:outline-none focus:ring-1 ${
      fieldErrors[field]
        ? 'border-red-500 focus:border-red-500 focus:ring-red-500'
        : 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
    }`;

  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 px-4">
      <div className="w-full max-w-md rounded-lg bg-white p-8 shadow-md">
        <h1 className="mb-6 text-center text-2xl font-bold text-gray-900">
          Crear Cuenta
        </h1>

        {error && (
          <div className="mb-4 rounded-md bg-red-50 p-3 text-sm text-red-700">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label htmlFor="nombre" className="block text-sm font-medium text-gray-700">
              Nombre
            </label>
            <input
              id="nombre"
              type="text"
              value={nombre}
              onChange={(e) => setNombre(e.target.value)}
              className={inputClass('nombre')}
              placeholder="Tu nombre"
            />
            {fieldErrors.nombre && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.nombre}</p>
            )}
          </div>

          <div>
            <label htmlFor="email" className="block text-sm font-medium text-gray-700">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className={inputClass('email')}
              placeholder="tu@email.com"
            />
            {fieldErrors.email && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.email}</p>
            )}
          </div>

          <div>
            <label htmlFor="password" className="block text-sm font-medium text-gray-700">
              Contraseña
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className={inputClass('password')}
              placeholder="••••••••"
            />
            {fieldErrors.password && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.password}</p>
            )}
          </div>

          <div>
            <label htmlFor="confirmPassword" className="block text-sm font-medium text-gray-700">
              Confirmar Contraseña
            </label>
            <input
              id="confirmPassword"
              type="password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className={inputClass('confirmPassword')}
              placeholder="••••••••"
            />
            {fieldErrors.confirmPassword && (
              <p className="mt-1 text-sm text-red-600">{fieldErrors.confirmPassword}</p>
            )}
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full rounded-md bg-indigo-600 px-4 py-2 font-medium text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-50"
          >
            {loading ? 'Creando cuenta...' : 'Crear Cuenta'}
          </button>
        </form>

        <p className="mt-4 text-center text-sm text-gray-600">
          ¿Ya tenés cuenta?{' '}
          <Link to="/login" className="text-indigo-600 hover:text-indigo-500">
            Iniciá sesión
          </Link>
        </p>
      </div>
    </div>
  );
}
