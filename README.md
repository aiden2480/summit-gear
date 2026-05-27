# Summit Gear — Climbing Equipment Store

## Summary

Climbing gear is typically sold through general outdoor retailers where it's buried alongside camping, cycling, and ski equipment, making it hard for climbers to browse a focused catalogue. Summit Gear is a lightweight single-page e-commerce application that solves this by providing a dedicated storefront for climbing equipment. Users must log in or register before accessing the store. Once authenticated, they can browse 34 products across 6 categories, filter by category, search, add items to a shopping cart, and complete a checkout process. The application features a dark mode UI with green accents, custom SVG icons, and smooth animations.

## Tech Stack

| Layer       | Technology                                      |
| ----------- | ----------------------------------------------- |
| Frontend    | React 19 (Vite)                                 |
| Styling     | Vanilla CSS with CSS custom properties          |
| Backend     | Python aiohttp (async HTTP framework)           |
| Database    | SQLite with SQLModel ORM                        |
| API         | RESTful JSON endpoints with CORS                |
| Auth        | JWT (PyJWT) with bcrypt password hashing        |

## Features

### Authentication & Sessions
- **Email/password authentication** — register and log in with bcrypt-hashed passwords and JWT (HS256, 24h expiry)
- **Role-based access** — `admin` and `user` roles enforced server-side on every protected endpoint
- **Persistent sessions** — `user`, `userId`, `token`, `role`, and `avatar` cached in `localStorage`
- **Cross-tab sync** — logging out in one tab logs out every open tab via the browser `storage` event
- **Auto-logout on 401** — a global `auth:unauthorized` event clears the session if the server rejects a token
- **Profile pictures** — users can upload a PNG/JPEG avatar (stored as bytes + MIME in the DB); generated colour gradients are used as a fallback

### Shop (user role)
- Browse 34 products across 6 categories with responsive grid
- Real-time client-side search by name or description
- Category filter pills
- Cart drawer with slide animation, quantity +/− controls, and per-line stock guard
- Live stock updates after every cart operation; out-of-stock cards greyscaled
- Checkout flow with atomic stock decrement and order confirmation modal
- Toast notifications for every success/error path

### Admin Dashboard (admin role)
- View, edit, and delete user accounts (email, role, avatar)
- Inspect any user's shopping cart in a read-only-style drawer with quantity controls
- Admin-only routes guarded server-side (not just by frontend role checks)

### UX & Accessibility
- Single-page client-side routing (React Router) — no full page reloads
- Dark mode UI with a green accent palette, custom SVG icons
- Keyboard navigation, ARIA labels, focus management on modals/drawers
- Connection-error fallback when backend is unreachable

## Authentication Flow

1. Unauthenticated visitors are redirected to `/login`; all shop routes are protected by `ProtectedRoute`
2. New users go to `/register` — credentials are validated (email format, lowercased), the password is bcrypt-hashed, and the account is stored
3. Returning users sign in on `/login` — the server verifies the bcrypt hash and issues a JWT signed with HS256
4. The JWT, user id, display name, role, and avatar are persisted to `localStorage` and mirrored into the React `AuthContext`
5. The header shows the avatar, name, and a **Sign Out** button
6. Admin role unlocks the **Admin** link in the header → `/admin` dashboard for user/cart management
7. The `storage` event listener in `AuthContext` keeps sibling tabs in sync; the `auth:unauthorized` event force-logs-out on 401 responses

## API Endpoints

### Auth (`routes/auth.py`)
| Operation | Resource | Endpoint              |
| --------- | -------- | --------------------- |
| Create    | Register | `POST /api/register`  |
| Create    | Login    | `POST /api/login`     |

### Products (`routes/products.py`)
| Operation | Resource    | Endpoint              |
| --------- | ----------- | --------------------- |
| Read      | Products    | `GET /api/products`   |
| Read      | Categories  | `GET /api/categories` |

### Cart (`routes/cart.py`)
| Operation | Resource              | Endpoint                       |
| --------- | --------------------- | ------------------------------ |
| Read      | Own cart              | `GET /api/cart`                |
| Create    | Cart item             | `POST /api/cart`               |
| Update    | Cart item qty         | `PUT /api/cart/{id}`           |
| Delete    | Cart item             | `DELETE /api/cart/{id}`        |
| Delete    | Clear own cart        | `DELETE /api/cart`             |
| Create    | Checkout              | `POST /api/checkout`           |
| Read      | User's cart (admin)   | `GET /api/cart/user/{user_id}` |

### User profile (`routes/user.py`)
| Operation | Resource     | Endpoint              |
| --------- | ------------ | --------------------- |
| Update    | Own profile  | `PUT /api/users/me`   |

### Admin (`routes/admin.py`, admin role required)
| Operation | Resource | Endpoint                       |
| --------- | -------- | ------------------------------ |
| Read      | Users    | `GET /api/users`               |
| Update    | User     | `PUT /api/users/{user_id}`     |
| Delete    | User     | `DELETE /api/users/{user_id}`  |

All `/api/*` endpoints except `/api/login` and `/api/register` require a `Bearer` JWT. Admin endpoints additionally verify the user's `role` server-side.

## Directory Structure

```
backend/
  app.py                    Entry point; registers all route modules + CORS
  requirements.txt          Python dependencies (aiohttp, SQLModel, PyJWT, bcrypt, …)
  database/
    __init__.py             Async engine + session factory; seeds products + admin/user accounts
    models.py               SQLModel tables: User, Product, CartItem (with relationships)
  routes/
    auth.py                 POST /api/login, POST /api/register
    products.py             Product & category reads
    cart.py                 User cart CRUD, checkout, admin "view user cart"
    user.py                 PUT /api/users/me (profile + avatar)
    admin.py                Admin-only user CRUD (role-gated)
    helpers.py              JWT decode, current-user lookup, role check decorators

frontend/
  index.html                Single HTML entry — the SPA mounts here
  package.json              Vite + React + react-router-dom + TS
  vite.config.js            Build config
  public/
    sunrise.svg             Logo / favicon
    backpack.svg            Cart icon
    pickup_truck.svg        Order success animation
    magnifying_glass.svg    Search icon
    package.svg             Empty results
  src/
    main.tsx                React root render
    App.tsx                 BrowserRouter + ProtectedRoute / ProtectedLoginRoute wiring
    App.css                 Global styles + CSS custom properties
    shared.css              Shared button styles & animations
    types.ts                Shared TS types (User, CartItem, UpdateUserPayload, ToastType)
    context/
      AuthContext.tsx       Auth state, login/logout, cross-tab storage sync, 401 listener
    services/
      api.ts                Typed fetch client, ApiError class, authApi / userApi / cartApi / adminApi
    hooks/
      useProducts.ts        Product fetch + filter
      useCart.ts            Cart state + mutation helpers
      useToast.ts           Toast queue
    components/
      HomePage.tsx          Authenticated shell — header + ShopPage / AdminDashboard
      ShopPage.tsx          Search + filters + product grid + cart drawer
      AdminDashboard.tsx    User list, edit/delete user, view user cart
      Login.tsx / .css      Login form (uses authApi.login)
      Register.tsx          Register form (uses authApi.register)
      Header.tsx / .css     Avatar, cart badge, admin link, sign-out
      Avatar.tsx / .css     User avatar (image or gradient initial)
      SearchBar.tsx / .css  Product search
      CategoryFilter.tsx / .css   Category pills
      Grid.tsx / .css       Generic responsive grid (loading state + empty state)
      Card.tsx / .css       Generic card base
      ProductGrid.tsx       Grid specialised for products
      ProductCard.tsx / .css  Product tile with add-to-cart
      UserGrid.tsx          Grid specialised for users
      UserCard.tsx / .css   User tile (admin dashboard)
      EditUserModal.tsx / .css  Edit email/role/avatar; used by admin and user profile
      CartDrawer.tsx / .css Slide-in cart panel (read-only mode for admin)
      CartItemEntry.tsx     Cart line item with qty +/− and remove
      OrderSuccess.tsx / .css   Checkout confirmation modal
      ConfirmDialog.tsx     Reusable confirmation modal
      Toast.tsx / .css      Toast notification component
      NoMatch.tsx           404 route
```

## Workload Allocation

Group members and the primary areas each member owns.

| Member         | GitHub handle  |
| -------------- | -------------- |
| Aiden Gardner  | `@aiden2480`   |
| Sophia Nguyen  | `@zfere`       |
| David Sorrell  | `@David-S-22`  |

---

### Sophia Nguyen (`@zfere`)

#### Backend Files
- `backend/database/models.py` — `User` model with role-based access (admin/user)
- `backend/routes/auth.py` — `POST /api/login` and `POST /api/register` with bcrypt password hashing, PyJWT HS256 token signing, email validation/normalisation
- `backend/routes/admin.py` — split admin-only endpoints (`GET/PUT/DELETE /api/users`) out of the main routes into a dedicated module
- `backend/database/__init__.py` — seed default `admin@example.com` and `user@example.com` accounts
- `backend/requirements.txt` — added `bcrypt`, `PyJWT` for auth

#### Frontend Files
- `frontend/src/context/AuthContext.tsx` — Auth state, `login` / `logout`, cross-tab `storage` event sync, `auth:unauthorized` 401 listener
- `frontend/src/components/Login.tsx` / `Login.css` — Login form, uses `authApi.login`
- `frontend/src/components/Register.tsx` — Register form, uses `authApi.register`, requires explicit sign-in after registration
- `frontend/src/components/Header.tsx` — User info, admin badge, sign-out button, cart-badge hide-when-empty fix
- `frontend/src/services/api.ts` — `ApiError` class, typed `authApi` / `cartApi` / `userApi` exports, multipart Content-Type guard, path-id fixes
- `frontend/src/types.ts` — `CartItem.user_id` rename (was misnamed `username`)
- `frontend/src/App.tsx` — `react-router-dom` migration with `ProtectedRoute` / `ProtectedLoginRoute` wrappers

#### Configuration & Documentation
- `README.md` — Authentication flow section, demo accounts, workload allocation

**Key Contributions:** Authentication system end-to-end (backend JWT + bcrypt, frontend `AuthContext`, role-based access control), React Router migration for SPA navigation, admin route module split, typed API client with `ApiError` class, cross-tab auth synchronisation, code-review fix sweep (email casing, `SubmitEvent` migration, multipart upload Content-Type guard, cart path-id bugs).

---

### David Sorrell (`@David-S-22`)

#### Backend Files
- `backend/app.py` — Added initial application structure, registered routes
- `backend/database/models.py` — Database model updates for admin dashboard
- `backend/routes/user.py` — User self-management endpoint (`PUT /api/users/me`)
- `backend/routes/cart.py` — Cart functionality for displaying user carts

#### Frontend Files
- `frontend/src/App.tsx` — Routing setup, separate user and admin landing pages
- `frontend/src/App.css` — Main application styling
- `frontend/src/components/AdminDashboard.tsx` — Admin dashboard with user view / cart functionality
- `frontend/src/components/Header.tsx` — Header component updates
- `frontend/src/components/HomePage.tsx` — Authenticated landing component
- `frontend/src/components/ShopPage.tsx` — Shop page component
- `frontend/src/components/Card.tsx` / `Card.css` — Reusable card base component
- `frontend/src/components/Grid.tsx` / `Grid.css` — Reusable grid base component
- `frontend/src/components/UserCard.tsx` / `UserCard.css` — User tile for admin dashboard
- `frontend/src/components/UserGrid.tsx` — User grid for admin dashboard
- `frontend/src/components/CartDrawer.tsx` / `CartDrawer.css` — Cart drawer admin-mode updates
- `frontend/src/components/CartItem.css` — Cart item styling
- `frontend/src/components/CartItemEntry.tsx` — Cart item entry component (renamed from CartItem)
- `frontend/src/global.d.ts` — Global TypeScript definitions
- `frontend/src/services/api.ts` — Extended for cart/user endpoints
- `frontend/src/types.ts` — Additional type definitions
- `frontend/vite.config.ts` — Vite configuration updates
- `frontend/package-lock.json` — Dependency updates

#### Configuration & Documentation
- `README.md` — Documentation updates

**Key Contributions:** Typescript migration, Admin dashboard development, user management features, admin cart viewing functionality, component library creation (Card, Grid, base components).

---

### Aiden Gardner (`@aiden2480`)

#### Backend Files
- `backend/app.py` — Application structure updates
- `backend/database/__init__.py` — Database initialisation and seeding
- `backend/database/models.py` — Comprehensive database models, SQLAlchemy ORM migration, foreign-key updates for cart items
- `backend/routes/auth.py` — Initial route file scaffolding and later refactors (admin decorator integration, user-id foreign-key updates after `CartItem` rename)
- `backend/routes/products.py` — Product routes, removed editing/deleting endpoints
- `backend/routes/cart.py` — Cart routes, checkout-decreases-stock logic, helper function extraction
- `backend/routes/helpers.py` — Helper functions for authentication and routing
- `backend/requirements.txt` — Initial backend dependency set; later additions for auth (`bcrypt`, `PyJWT`, `passlib`) were added in commits authored by other members

#### Frontend Files
- `frontend/src/App.jsx` → `App.tsx` — Main app, page transitions, product refresh on checkout
- `frontend/src/main.jsx` → `main.tsx` — Application entry point
- `frontend/src/services/api.js` → `api.ts` — API service layer, cart/product endpoints
- `frontend/vite.config.js` → `vite.config.ts` — Vite configuration
- `frontend/src/types.ts` — TypeScript type definitions
- `frontend/src/vite-env.d.ts` — Vite environment types
- `frontend/src/components/CartDrawer.jsx` → `.tsx` / `.css` — Cart drawer, SVG icons, condensed CSS
- `frontend/src/components/CartItem.jsx` → `.tsx` / `.css` — Cart item component (later renamed)
- `frontend/src/components/Header.jsx` → `.tsx` / `.css` — Header with SVG icons
- `frontend/src/components/OrderSuccess.jsx` → `.tsx` / `.css` — Order success modal
- `frontend/src/components/ProductCard.jsx` → `.tsx` / `.css` — Product card
- `frontend/src/components/ProductGrid.jsx` → `.tsx` / `.css` — Product grid
- `frontend/src/components/ProductModal.jsx` / `.css` — Product modal (later removed)
- `frontend/src/components/SearchBar.jsx` → `.tsx` / `.css` — Search bar with debouncing
- `frontend/src/components/CategoryFilter.jsx` → `.tsx` / `.css` — Category filter
- `frontend/src/components/Toast.jsx` → `.tsx` / `.css` — Toast notifications
- `frontend/src/shared.css` — Shared styling utilities
- `frontend/src/App.css` — App-wide styling, colour variables
- `frontend/src/hooks/useCart.js` → `useCart.ts` — Cart hook
- `frontend/src/hooks/useProducts.js` → `useProducts.ts` — Products hook
- `frontend/src/hooks/useToast.js` → `useToast.ts` — Toast hook
- `frontend/index.html` — HTML entry, SVG icons
- `frontend/eslint.config.js` — ESLint config
- `frontend/tsconfig.json` — TypeScript config
- `frontend/package.json` / `package-lock.json` — Dependencies and scripts

#### Assets
- `frontend/public/magnifying_glass.svg`, `package.svg`, `shopping_cart.svg`, `backpack.svg`, `sunrise.svg`, `climbing.svg`
- Replaced multiple product images with climbing-gear photos

#### Configuration & Documentation
- `README.md` — Documentation, rubric-aligned comments
- `.github/workflows/frontend-build.yml` — GitHub Actions CI workflow

**Key Contributions:** Project scaffolding and database architecture (SQLAlchemy ORM migration, `User`/`Product`/`CartItem` model relationships, foreign-key updates), comprehensive `.jsx` → `.tsx` TypeScript migration across the frontend, shop UI components (cart drawer, product grid/card, search, category filter, toasts, header), checkout flow with atomic stock decrement, styling/theming system with CSS variables, climbing-gear asset set, profile pictures feature, GitHub Actions CI/CD setup.

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

The server starts at `http://localhost:8080`. The database is created and seeded automatically on first run.

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

The development server starts at `http://localhost:5173`.
