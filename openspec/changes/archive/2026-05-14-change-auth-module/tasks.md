## 1. Backend — Auth Schemas

- [x] 1.1 Create `auth/schemas.py` with request DTOs: `RegisterRequest` (nombre, email, password), `LoginRequest` (email, password), `RefreshRequest` (refresh_token)
- [x] 1.2 Create response DTOs: `AuthResponse` (access_token, refresh_token, user: UserRead), `TokenRefreshResponse` (access_token, refresh_token)
- [x] 1.3 Add Pydantic validations: email format (email_validator), password min_length=8, nombre min_length=2

## 2. Backend — RefreshToken Repository

- [x] 2.1 Create `auth/repository.py` with `RefreshTokenRepository` extending `BaseRepository[RefreshTokenModel]`
- [x] 2.2 Implement `create_token(user_id, token_id, family_id, expires_at)` to store a new refresh token record
- [x] 2.3 Implement `find_by_token_id(token_id)` to look up a refresh token by its JTI
- [x] 2.4 Implement `revoke_token(token_id)` to set `revoked=True` on a specific token
- [x] 2.5 Implement `revoke_family(family_id)` to set `revoked=True` on ALL tokens in a family (replay attack)
- [x] 2.6 Implement `get_active_by_user(user_id)` to list non-revoked tokens for a user

## 3. Backend — Auth Service

- [x] 3.1 Create `auth/service.py` with `AuthService` class accepting UnitOfWork via constructor
- [x] 3.2 Implement `register(nombre, email, password)`: validate email unique, hash password, create Usuario with CLIENT role, generate token pair, store refresh token, return AuthResponse
- [x] 3.3 Implement `login(email, password)`: find user by email, verify password (generic 401 if either fails), generate token pair, store refresh token, return AuthResponse
- [x] 3.4 Implement `refresh(refresh_token_str)`: decode JWT, find token in DB, check if revoked → if revoked trigger `revoke_family`, if valid: revoke old token, create new, return TokenRefreshResponse
- [x] 3.5 Implement `logout(refresh_token_str)`: decode JWT, find token in DB, revoke it
- [x] 3.6 Ensure login response does NOT differentiate between "email not found" and "wrong password" (generic "Credenciales inválidas")

## 4. Backend — Auth Router with Rate Limiting

- [x] 4.1 Implement `POST /api/v1/auth/register` with `@limiter.limit("3/hour")`, call AuthService.register
- [x] 4.2 Implement `POST /api/v1/auth/login` with `@limiter.limit("5/minute")`, call AuthService.login
- [x] 4.3 Implement `POST /api/v1/auth/refresh` with `@limiter.limit("10/minute")`, call AuthService.refresh
- [x] 4.4 Implement `POST /api/v1/auth/logout` (authenticated), call AuthService.logout
- [x] 4.5 Add `Limiter` injection via `Depends(limiter)` to all auth endpoints with rate limits
- [x] 4.6 Ensure rate limit exceeded responses include `Retry-After` header

## 5. Frontend — Login Page

- [x] 5.1 Create `frontend/src/pages/Login.tsx` with email/password form fields using useState
- [x] 5.2 Implement form submission: call `POST /api/v1/auth/login` via Axios, store tokens in authStore, redirect to dashboard on success
- [x] 5.3 Display inline error messages for invalid credentials and rate limiting (429)
- [x] 5.4 Add loading state on submit button (disabled + spinner/text)
- [x] 5.5 Add link to navigate to `/register`
- [x] 5.6 Add route for `/login` in App.tsx router configuration

## 6. Frontend — Register Page

- [x] 6.1 Create `frontend/src/pages/Register.tsx` with name/email/password/confirm-password form fields using useState
- [x] 6.2 Implement client-side validation: password min 8 chars, passwords match, email format, nombre min 2 chars
- [x] 6.3 Implement form submission: call `POST /api/v1/auth/register` via Axios, store tokens in authStore, redirect to dashboard on success
- [x] 6.4 Display inline error messages for validation errors and duplicate email (409)
- [x] 6.5 Add loading state on submit button
- [x] 6.6 Add link to navigate to `/login`
- [x] 6.7 Add route for `/register` in App.tsx router configuration

## 7. Frontend — Conditional Navigation

- [x] 7.1 Update App.tsx or Layout component to show different navigation based on `authStore.isAuthenticated`
- [x] 7.2 When authenticated: show user name, link to profile (placeholder), logout button
- [x] 7.3 When not authenticated: show "Iniciar sesión" and "Registrarse" links
- [x] 7.4 Implement logout handler: call `POST /api/v1/auth/logout`, clear authStore, redirect to home
- [x] 7.5 Add `PrivateLayout` auth guard: redirect to `/login` if not authenticated (resolve the TODO from Sprint 0)
