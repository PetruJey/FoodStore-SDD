## ADDED Requirements

### Requirement: authStore
The system SHALL have authStore with: accessToken, refreshToken, user (id, nombre, email, roles), isAuthenticated; actions: login(), logout(), updateTokens(); selectors: isAuthenticated(), hasRole(); persistence in localStorage key "food-store-auth"

#### Scenario: authStore initial state
- **WHEN** the store initializes
- **THEN** accessToken, refreshToken, and user SHALL be restored from localStorage key "food-store-auth", and isAuthenticated SHALL reflect whether a token exists

#### Scenario: login updates state
- **WHEN** calling `login({ accessToken, refreshToken, user })`
- **THEN** authStore SHALL update accessToken, refreshToken, user, and isAuthenticated

#### Scenario: logout clears state
- **WHEN** calling `logout()`
- **THEN** authStore SHALL clear accessToken, refreshToken, and user, set isAuthenticated to false, and remove data from localStorage

#### Scenario: hasRole selector
- **WHEN** calling `hasRole(["admin"])`
- **THEN** it SHALL return true if user has "admin" role, false otherwise

### Requirement: cartStore
The system SHALL have cartStore with: items array; actions: addItem(), removeItem(), updateQuantity(), clearCart(); selectors: totalItems(), totalPrice(), getItem(); persistence in localStorage key "food-store-cart"

#### Scenario: addItem adds to cart
- **WHEN** calling `addItem({ id: 1, nombre: "Producto", precio: 100 })`
- **THEN** the item SHALL appear in the items array

#### Scenario: removeItem removes from cart
- **WHEN** calling `removeItem(1)`
- **THEN** the item with id=1 SHALL be removed from items

#### Scenario: updateQuantity changes quantity
- **WHEN** calling `updateQuantity(1, 3)`
- **THEN** the item with id=1 SHALL have quantity set to 3

#### Scenario: clearCart empties items
- **WHEN** calling `clearCart()`
- **THEN** the items array SHALL be empty

#### Scenario: totalItems selector
- **WHEN** calling `totalItems()`
- **THEN** it SHALL return the sum of all item quantities

#### Scenario: totalPrice selector
- **WHEN** calling `totalPrice()`
- **THEN** it SHALL return the sum of (precio * quantity) for all items

#### Scenario: cartStore persistence
- **WHEN** the store initializes
- **THEN** cart items SHALL be restored from localStorage key "food-store-cart"

### Requirement: paymentStore
The system SHALL have paymentStore with: checkoutStep, preferenceId, paymentStatus, error; actions: startCheckout(), setPreference(), updatePaymentStatus(), resetPayment(); NO persistence (transient state)

#### Scenario: startCheckout initializes
- **WHEN** calling `startCheckout()`
- **THEN** checkoutStep SHALL be set to the initial step and previous state SHALL be cleared

#### Scenario: setPreference stores preference
- **WHEN** calling `setPreference("pref_id")`
- **THEN** preferenceId SHALL be set to "pref_id"

#### Scenario: updatePaymentStatus updates status
- **WHEN** calling `updatePaymentStatus("approved")`
- **THEN** paymentStatus SHALL be set to "approved"

#### Scenario: resetPayment clears state
- **WHEN** calling `resetPayment()`
- **THEN** checkoutStep, preferenceId, paymentStatus, and error SHALL be reset to defaults

#### Scenario: paymentStore not persisted
- **WHEN** the store initializes
- **THEN** it SHALL NOT read from or write to localStorage

### Requirement: uiStore
The system SHALL have uiStore with: theme (light/dark), sidebarOpen, toasts; persistence selective: only theme persisted

#### Scenario: uiStore default state
- **WHEN** the store initializes
- **THEN** theme SHALL be restored from localStorage, sidebarOpen SHALL default to false, and toasts SHALL default to empty array

#### Scenario: Toggle theme
- **WHEN** toggling the theme
- **THEN** uiStore SHALL update theme and persist it to localStorage

#### Scenario: Toasts not persisted
- **WHEN** adding a toast
- **THEN** it SHALL appear in the toasts array but SHALL NOT be written to localStorage

### Requirement: Slice subscriptions
The system SHALL have all stores using slice subscriptions (not full useStore())

#### Scenario: Slice selectors used
- **WHEN** a component subscribes to a store
- **THEN** it SHALL subscribe to specific slices (e.g., `useAuthStore(state => state.isAuthenticated)`) rather than the full store object
