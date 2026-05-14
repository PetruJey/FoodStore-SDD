## ADDED Requirements

### Requirement: Login page
The system SHALL have a login page at `/login` with email and password form fields.

#### Scenario: Successful login flow
- **WHEN** a user enters valid credentials and submits the login form
- **THEN** the system SHALL call `POST /api/v1/auth/login` via Axios
- **AND** the system SHALL store the tokens and user data in authStore
- **AND** the system SHALL redirect the user to the dashboard

#### Scenario: Login error display
- **WHEN** login fails due to invalid credentials
- **THEN** the system SHALL display the error message "Credenciales inválidas" on the form
- **AND** the system SHALL NOT redirect

#### Scenario: Login rate limit display
- **WHEN** login fails due to rate limiting (HTTP 429)
- **THEN** the system SHALL display a message indicating too many attempts and the retry time

#### Scenario: Login loading state
- **WHEN** the login request is in progress
- **THEN** the submit button SHALL show a loading state and be disabled

#### Scenario: Navigate to register
- **WHEN** a user clicks "¿No tenés cuenta? Registrate"
- **THEN** the system SHALL navigate to `/register`

### Requirement: Register page
The system SHALL have a registration page at `/register` with name, email, password and confirm password fields.

#### Scenario: Successful registration flow
- **WHEN** a user fills valid data and submits the registration form
- **THEN** the system SHALL call `POST /api/v1/auth/register` via Axios
- **AND** the system SHALL store the tokens and user data in authStore
- **AND** the system SHALL redirect the user to the dashboard

#### Scenario: Registration validation errors
- **WHEN** the form has validation errors (short password, invalid email, passwords don't match)
- **THEN** the system SHALL display inline validation messages
- **AND** the system SHALL NOT submit the form

#### Scenario: Duplicate email on register
- **WHEN** the backend returns HTTP 409 for duplicate email
- **THEN** the system SHALL display "Este email ya está registrado" on the form

#### Scenario: Navigate to login
- **WHEN** a user clicks "¿Ya tenés cuenta? Iniciá sesión"
- **THEN** the system SHALL navigate to `/login`

### Requirement: Conditional navigation
The system SHALL show different navigation options based on authentication state.

#### Scenario: Authenticated user sees profile and logout
- **WHEN** a user is authenticated (`isAuthenticated` is true in authStore)
- **THEN** the navigation SHALL show the user's name, a link to profile, and a logout button

#### Scenario: Unauthenticated user sees login and register
- **WHEN** a user is not authenticated
- **THEN** the navigation SHALL show "Iniciar sesión" and "Registrarse" links

#### Scenario: Logout action
- **WHEN** an authenticated user clicks the logout button
- **THEN** the system SHALL call `POST /api/v1/auth/logout` with the current refresh token
- **AND** the system SHALL clear authStore and localStorage
- **AND** the system SHALL redirect to the home page
