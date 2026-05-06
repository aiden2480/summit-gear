# Summit Gear — Climbing Equipment Store

## Summary

Summit Gear is a single-page e-commerce application themed around rock climbing gear. Users must log in or register before accessing the store. Once authenticated, they can browse 34 products across 6 categories, filter by category, search, add items to a shopping cart, and complete a checkout process. The application features a dark mode UI with green accents, custom SVG icons, and smooth animations.

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

- **User authentication** — register and login with bcrypt-hashed passwords and JWT tokens
- **Persistent sessions** — JWT and username stored in `localStorage`, surviving page refreshes
- Dark mode UI with muted green accent colour scheme
- Custom SVG icons throughout
- Product browsing with responsive grid layout
- Category filtering with dynamic pill buttons
- Real-time product search by name or description
- Shopping cart drawer with slide transition and quantity controls
- Stock tracking with out-of-stock greyscale effect and low-stock indicators
- Real-time stock updates on cart changes
- Checkout flow with order confirmation modal
- Toast notifications for user feedback
- Responsive design
- Keyboard navigation and ARIA labels

## Authentication Flow

1. On first visit, the app renders the **Login** screen (no shop is visible without an account)
2. New users click **Sign Up** to switch to the **Register** screen — credentials are hashed with bcrypt and stored in the database, and a signed JWT is returned
3. Returning users enter their credentials on the **Login** screen — the server verifies the password hash and issues a fresh JWT
4. The JWT and username are saved to `localStorage` and the shop loads immediately
5. The header shows the logged-in username and a **Sign Out** button that clears the session

## API Endpoints

### Auth

| Operation | Resource  | Endpoint         |
| --------- | --------- | ---------------- |
| Create    | Register  | POST /register   |
| Create    | Login     | POST /login      |

### Shop

| Operation | Resource     | Endpoint                 |
| --------- | ------------ | ------------------------ |
| Read      | Products     | GET /api/products        |
| Read      | Categories   | GET /api/categories      |
| Create    | Cart Items   | POST /api/cart           |
| Read      | Cart         | GET /api/cart            |
| Update    | Cart Items   | PUT /api/cart/{id}       |
| Delete    | Cart Items   | DELETE /api/cart/{id}    |
| Delete    | Cart         | DELETE /api/cart         |
| Create    | Checkout     | POST /api/checkout       |

## Directory Structure

```
backend/
  app.py                  Entry point, sets up routes and CORS
  requirements.txt        Python dependencies
  database/
    __init__.py           Session factory, engine setup, seed data
    models.py             SQLModel models (Product, CartItem, User)
  routes/
    auth.py               Login and register endpoints (JWT + bcrypt)
    products.py           Product and category API endpoints
    cart.py               Cart and checkout endpoints

frontend/
  index.html              HTML entry point
  package.json            npm scripts and dependencies
  vite.config.js          Build configuration
  public/
    sunrise.svg           Logo and favicon
    backpack.svg          Cart icon and empty cart
    pickup_truck.svg      Order success animation
    magnifying_glass.svg  Search bar icon
    package.svg           Empty results icon
  src/
    main.tsx              React DOM render
    App.tsx               Root component — manages auth state, renders Login/Register/Shop
    App.css               Global styles and CSS variables
    shared.css            Shared button styles and animations
    services/
      api.ts              API client (request helpers)
    hooks/
      useProducts.ts      Product fetching and filtering
      useCart.ts          Cart state management
      useToast.ts         Toast notification state
    components/
      Login.tsx/.css      Login form
      Register.tsx        Register form (shares Login.css)
      Header.tsx/.css     Navigation with cart badge, username, and sign-out
      SearchBar.tsx/.css  Product search input
      CategoryFilter.tsx/.css  Category filter pills
      ProductGrid.tsx/.css     Product list container
      ProductCard.tsx/.css     Individual product card
      CartDrawer.tsx/.css      Slide-in cart panel
      CartItem.tsx/.css        Cart line item
      OrderSuccess.tsx/.css    Checkout confirmation modal
      Toast.tsx/.css           Notification component
```

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

## Key Implementation Details

The backend uses SQLModel with aiosqlite for async database access. Product data is seeded from the database module on first run with 34 climbing gear products across 6 categories (Protection, Ropes & Slings, Hardware, Harnesses, Footwear, Apparel). The checkout endpoint atomically reduces stock for all cart items before clearing the cart.

Authentication uses `passlib` with the bcrypt scheme to hash passwords before storing them, and `PyJWT` to sign tokens with an HS256 signature. Tokens expire after 24 hours. The frontend reads `user` and `token` from `localStorage` on startup — if either is missing the shop is replaced with the Login screen. The `App` component manages a single `user` state value; setting it to `null` (on sign-out) immediately shows the Login screen again without a page reload.

The frontend uses React hooks for state management without additional libraries. Stock counts update in real-time after every cart operation. All colours are defined as CSS custom properties for easy theming, and shared patterns (buttons, animations) are consolidated into a single shared stylesheet.

## Challenges Overcome

The biggest challenge in this project was managing the cart state and ensuring the UI stayed in sync with the backend stock levels. I designed the API endpoints to handle concurrent updates and ensure that the frontend re-fetches product data after every cart change to reflect accurate stock counts.
Another challenge was implementing the checkout flow with proper error handling for out-of-stock items. I had to ensure that the backend checks stock levels before confirming an order and that the frontend provides clear feedback to the user if an item becomes unavailable during checkout.
Integrating authentication as a single-page overlay (rather than a separate route) required threading auth state through the component tree without a router. The solution was to manage `user` at the `App` level and conditionally render the Login/Register screens or the shop based on that single piece of state.
