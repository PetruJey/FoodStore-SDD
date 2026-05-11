## ADDED Requirements

### Requirement: React + Vite + TypeScript project scaffold
The frontend SHALL be a React application built with Vite and TypeScript.

#### Scenario: Dev server starts without errors
- **WHEN** running `npm run dev`
- **THEN** the dev server SHALL start at `http://localhost:5173`
- **AND** the application SHALL render without console errors

#### Scenario: TypeScript configuration
- **WHEN** inspecting `tsconfig.json`
- **THEN** it SHALL have `strict: true` mode enabled
- **AND** use path aliases for `@/` mapping to `src/`

### Requirement: Feature-Sliced Design directory structure
The frontend SHALL follow Feature-Sliced Design with 4 layers: pages, features, entities, shared.

#### Scenario: FSD layers exist
- **WHEN** inspecting the `frontend/src/` directory
- **THEN** it SHALL contain `app/`, `pages/`, `features/`, `entities/`, `shared/`, and `hooks/` directories

#### Scenario: Import boundaries respected
- **WHEN** reviewing imports across layers
- **THEN** pages MAY import from features, entities, shared
- **AND** features MAY import from entities, shared
- **AND** entities MAY import from shared only
- **AND** shared SHALL NOT import from any other layer

### Requirement: Tailwind CSS configuration
The frontend SHALL use Tailwind CSS for styling.

#### Scenario: Tailwind is configured
- **WHEN** inspecting `tailwind.config.js`
- **THEN** it SHALL scan `./src/**/*.{ts,tsx}` for class usage

#### Scenario: Global styles exist
- **WHEN** inspecting `src/index.css`
- **THEN** it SHALL include Tailwind directives (`@tailwind base`, `@tailwind components`, `@tailwind utilities`)

### Requirement: Axios HTTP client with JWT interceptors
The frontend SHALL include a preconfigured Axios instance.

#### Scenario: Axios instance configured
- **WHEN** importing the API client
- **THEN** the base URL SHALL be read from `VITE_API_BASE_URL` environment variable
- **AND** the instance SHALL include a request interceptor that attaches the JWT `Authorization: Bearer <token>` header

#### Scenario: Response interceptor for token refresh
- **WHEN** a request returns 401
- **THEN** the interceptor SHALL attempt to refresh the token using the stored refresh token
- **AND** retry the original request with the new access token
- **AND** if refresh fails, SHALL clear auth state and redirect to login

### Requirement: Zustand stores for client state
The frontend SHALL use Zustand for client-side state management.

#### Scenario: Auth store exists
- **WHEN** inspecting stores
- **THEN** there SHALL be an `authStore` managing user session state (token, user data, login/logout actions)

#### Scenario: Cart store exists
- **WHEN** inspecting stores
- **THEN** there SHALL be a `cartStore` managing shopping cart state (items, add/remove/update quantity, total calculation)

#### Scenario: Cart persists to localStorage
- **WHEN** items are added to the cart and the page is refreshed
- **THEN** the cart state SHALL be restored from localStorage

### Requirement: TanStack Query provider
The frontend SHALL include TanStack Query for server state management.

#### Scenario: QueryClient provider wraps the app
- **WHEN** inspecting the app component tree
- **THEN** the root SHALL be wrapped in a `QueryClientProvider`
- **AND** the provider SHALL include a configured `QueryClient` with sensible defaults (staleTime: 5 minutes, retry: 2)

### Requirement: React Router setup
The frontend SHALL use React Router for client-side routing.

#### Scenario: Routes defined
- **WHEN** inspecting the router configuration
- **THEN** it SHALL define routes for: home (`/`), products (`/productos`), cart (`/carrito`), checkout (`/checkout`), login (`/login`), register (`/registro`), admin dashboard (`/admin`), and user profile (`/perfil`)

#### Scenario: Root App component renders
- **WHEN** inspecting `src/app/App.tsx`
- **THEN** it SHALL compose the providers (QueryClientProvider) and router
- **AND** serve as the root component rendered by `main.tsx`

### Requirement: ESLint and Prettier configuration
The frontend SHALL include code quality tooling.

#### Scenario: ESLint configured
- **WHEN** inspecting the project
- **THEN** there SHALL be an ESLint configuration for TypeScript and React with recommended rulesets

#### Scenario: Prettier configured
- **WHEN** inspecting the project
- **THEN** there SHALL be a Prettier configuration for consistent code formatting

### Requirement: Entry point exists
The frontend SHALL have a proper entry point.

#### Scenario: main.tsx renders App
- **WHEN** inspecting `src/main.tsx`
- **THEN** it SHALL render the App component into the DOM
- **AND** use `StrictMode` wrapper
