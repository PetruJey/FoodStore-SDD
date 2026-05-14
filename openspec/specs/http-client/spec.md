## ADDED Requirements

### Requirement: Centralized Axios instance
The system SHALL have Axios instance centralized in shared/api/axios.ts

#### Scenario: Axios instance exported
- **WHEN** importing `shared/api/axios.ts`
- **THEN** a configured Axios instance SHALL be available for import

### Requirement: Access token interceptor
The system SHALL have request interceptor attaching access token from authStore as Authorization: Bearer <token>

#### Scenario: Request interceptor adds token
- **WHEN** a request is made through the Axios instance
- **THEN** the request interceptor SHALL attach `Authorization: Bearer <token>` header using the token from authStore

### Requirement: Token refresh interceptor
The system SHALL have response interceptor catching 401, attempting token refresh using refresh token, updating authStore, and retrying original request

#### Scenario: 401 triggers refresh
- **WHEN** a 401 response is received
- **THEN** the interceptor SHALL attempt to refresh the token using the stored refresh token, update authStore with new tokens, and retry the original request

#### Scenario: Refresh fails
- **WHEN** the refresh request also returns a 401
- **THEN** the interceptor SHALL log the user out and reject the original request

### Requirement: Base URL from env
The system SHALL have base URL coming from VITE_API_BASE_URL env var

#### Scenario: Base URL configured
- **WHEN** the Axios instance is created
- **THEN** `baseURL` SHALL be set to the value of `VITE_API_BASE_URL` environment variable
