## ADDED Requirements

### Requirement: Vite + React + TypeScript
The system SHALL have a Vite + React + TypeScript project with SWC plugin

#### Scenario: Project scaffolded with Vite
- **WHEN** inspecting the frontend project
- **THEN** `vite.config.ts` SHALL exist with React SWC plugin configured

### Requirement: Strict TypeScript
The system SHALL have TypeScript configured with strict: true

#### Scenario: Strict mode enabled
- **WHEN** inspecting `tsconfig.json`
- **THEN** `compilerOptions.strict` SHALL be set to `true`

### Requirement: Tailwind CSS v3+
The system SHALL have Tailwind CSS v3+ configured with PostCSS and production purging

#### Scenario: Tailwind config exists
- **WHEN** inspecting the frontend project
- **THEN** `tailwind.config.js` SHALL exist with content paths for production purging

#### Scenario: PostCSS configured
- **WHEN** inspecting the frontend project
- **THEN** `postcss.config.js` SHALL exist with Tailwind and autoprefixer plugins

### Requirement: React Router setup
The system SHALL have react-router-dom configured with public and private routes

#### Scenario: Router configured
- **WHEN** inspecting the app entry point
- **THEN** react-router-dom SHALL be configured with separate layouts for public and private (authenticated) routes

### Requirement: TanStack Query
The system SHALL have TanStack Query configured with QueryClientProvider at App root

#### Scenario: QueryClientProvider wraps app
- **WHEN** inspecting the app root component
- **THEN** `QueryClientProvider` SHALL wrap the entire application with a configured `QueryClient`

### Requirement: npm dependencies
The system SHALL have npm dependencies including: react, react-dom, react-router-dom, @tanstack/react-query, @tanstack/react-form, zustand, axios, recharts, tailwindcss, @mercadopago/sdk-js

#### Scenario: Dependencies in package.json
- **WHEN** inspecting `package.json`
- **THEN** all specified dependencies SHALL be listed

### Requirement: Dev dependencies
The system SHALL have dev dependencies including: typescript, @types/react, @types/react-dom, vite, @vitejs/plugin-react-swc, tailwindcss, postcss, autoprefixer

#### Scenario: Dev dependencies in package.json
- **WHEN** inspecting `package.json`
- **THEN** all specified dev dependencies SHALL be listed

### Requirement: Env example
The system SHALL have .env.example with VITE_API_BASE_URL and VITE_MERCADOPAGO_PUBLIC_KEY

#### Scenario: Env example exists
- **WHEN** inspecting the frontend root
- **THEN** `.env.example` SHALL exist with `VITE_API_BASE_URL=http://localhost:8000/api/v1` and `VITE_MERCADOPAGO_PUBLIC_KEY=TEST-xxx`
