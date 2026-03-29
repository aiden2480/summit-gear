# ShopWave — E-commerce Shopping Cart

## Summary

ShopWave is a single-page e-commerce application that allows users to browse products, filter by category, search, add items to a shopping cart, and complete a checkout process. The application demonstrates full CRUD operations on a database with a focus on a smooth, responsive user experience.

## Tech Stack

| Layer       | Technology                                      |
| ----------- | ----------------------------------------------- |
| Frontend    | React 19 (Vite)                                 |
| Styling     | Vanilla CSS with CSS custom properties          |
| Backend     | Python aiohttp (async HTTP framework)           |
| Database    | SQLite with async SQLAlchemy ORM                |
| API         | RESTful JSON endpoints with CORS                |

## Features

- Product browsing with responsive grid layout
- Category filtering with dynamic pill buttons
- Real-time product search by name or description
- Shopping cart drawer with quantity controls
- Stock tracking with out-of-stock and low-stock indicators
- Checkout flow with order confirmation and random order ID generation
- Stock reduction on successful checkout
- Toast notifications for user feedback
- Responsive design with mobile-first approach
- Keyboard navigation and ARIA labels
- Smooth animations and transitions

## CRUD Operations

| Operation | Resource     | Endpoint                 |
| --------- | ------------ | ------------------------ |
| Read      | Products     | GET /api/products        |
| Create    | Cart Items   | POST /api/cart           |
| Read      | Cart         | GET /api/cart            |
| Update    | Cart Items   | PUT /api/cart/{id}       |
| Delete    | Cart Items   | DELETE /api/cart/{id}    |
| Delete    | Cart         | DELETE /api/cart         |
| POST      | Checkout     | POST /api/checkout       |

## Directory Structure

```
backend/
  app.py                  Entry point, sets up routes and CORS
  requirements.txt        Python dependencies
  database/
    __init__.py          Session factory and engine setup
    models.py            SQLAlchemy ORM models (Product, CartItem)
  routes/
    products.py          Product API endpoints
    cart.py              Cart and checkout endpoints

frontend/
  index.html             HTML entry point
  package.json           npm scripts and dependencies
  vite.config.js         Build configuration
  src/
    main.jsx             React DOM render
    App.jsx              Root component
    App.css              Global styles
    services/
      api.js             API client (request helpers)
    hooks/
      useProducts.js     Product fetching and filtering
      useCart.js         Cart state management
      useToast.js        Toast notification state
    components/
      Header.jsx         Navigation with cart badge
      SearchBar.jsx      Product search input
      CategoryFilter.jsx Category filter pills
      ProductGrid.jsx    Product list container
      ProductCard.jsx    Individual product card
      CartDrawer.jsx     Slide-in cart panel
      CartItem.jsx       Cart line item
      OrderSuccess.jsx   Checkout confirmation
      Toast.jsx          Notification component
```

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+

### Backend Setup

```bash
cd backend
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

The backend uses async SQLAlchemy with aiosqlite to handle concurrent requests efficiently. Product data is read-only and seeded from JSON on startup. The checkout endpoint atomically reduces stock for all cart items before clearing the cart, ensuring consistency. The frontend uses React hooks for state management without additional libraries. The cart drawer implements smooth CSS transitions with React state for seamless UX. All API errors are handled gracefully with toast notifications to provide clear user feedback.
