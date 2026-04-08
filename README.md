# Summit Gear — Climbing Equipment Store

## Summary

Summit Gear is a single-page e-commerce application themed around rock climbing gear. Users can browse 34 products across 6 categories, filter by category, search, add items to a shopping cart, and complete a checkout process. The application features a dark mode UI with green accents, custom SVG icons, and smooth animations.

## Tech Stack

| Layer       | Technology                                      |
| ----------- | ----------------------------------------------- |
| Frontend    | React 19 (Vite)                                 |
| Styling     | Vanilla CSS with CSS custom properties          |
| Backend     | Python aiohttp (async HTTP framework)           |
| Database    | SQLite with SQLModel ORM                        |
| API         | RESTful JSON endpoints with CORS                |

## Features

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

## CRUD Operations

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
    models.py             SQLModel models (Product, CartItem)
  routes/
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
    main.jsx              React DOM render
    App.jsx               Root component with state management
    App.css               Global styles and CSS variables
    shared.css            Shared button styles and animations
    services/
      api.js              API client (request helpers)
    hooks/
      useProducts.js      Product fetching and filtering
      useCart.js           Cart state management
      useToast.js         Toast notification state
    components/
      Header.jsx/.css     Navigation with cart badge
      SearchBar.jsx/.css  Product search input
      CategoryFilter.jsx/.css  Category filter pills
      ProductGrid.jsx/.css     Product list container
      ProductCard.jsx/.css     Individual product card
      CartDrawer.jsx/.css      Slide-in cart panel
      CartItem.jsx/.css        Cart line item
      OrderSuccess.jsx/.css    Checkout confirmation modal
      Toast.jsx/.css           Notification component
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

The backend uses SQLModel with aiosqlite for async database access. Product data is seeded from the database module on first run with 34 climbing gear products across 6 categories (Protection, Ropes & Slings, Hardware, Harnesses, Footwear, Apparel). The checkout endpoint atomically reduces stock for all cart items before clearing the cart. The frontend uses React hooks for state management without additional libraries. Stock counts update in real-time after every cart operation. All colours are defined as CSS custom properties for easy theming, and shared patterns (buttons, animations) are consolidated into a single shared stylesheet.

## Challenges Overcome

The biggest challenge in this project was managing the cart state and ensuring the UI stayed in sync with the backend stock levels. I designed the API endpoints to handle concurrent updates and ensure that the frontend re-fetches product data after every cart change to reflect accurate stock counts.
Another challenge was implementing the checkout flow with proper error handling for out-of-stock items. I had to ensure that the backend checks stock levels before confirming an order and that the frontend provides clear feedback to the user if an item becomes unavailable during checkout.
