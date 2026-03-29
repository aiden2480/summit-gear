# ShopWave — E-commerce Shopping Cart

## Summary

ShopWave is a single-page e-commerce shopping cart application that allows users to browse products, filter by category, search, and manage a shopping cart. It demonstrates full CRUD (Create, Read, Update, Delete) operations on a database through a polished, responsive web interface.

## Tech Stack

| Layer       | Technology                                |
| ----------- | ----------------------------------------- |
| Frontend    | React 19 (via Vite)                       |
| Styling     | Vanilla CSS with CSS custom properties    |
| Backend     | Python aiohttp.web (async HTTP framework) |
| Database    | SQLite (via aiosqlite)                     |
| API         | RESTful JSON endpoints with CORS support  |

## Features

- **Product Browsing** — responsive grid of product cards with images, prices, and stock indicators
- **Category Filtering** — filter products by category with pill-style toggle buttons
- **Product Search** — real-time search bar that filters products by name or description
- **Shopping Cart Drawer** — slide-in cart panel with quantity controls and running total
- **Product Management** — add, edit, and delete products via a modal dialog (full CRUD)
- **Stock Tracking** — out-of-stock and low-stock badges; quantity capped to available stock
- **Toast Notifications** — animated success/error feedback for every user action
- **Responsive Design** — mobile-first layout that adapts from phone to desktop
- **Accessibility** — ARIA labels, keyboard navigability, focus outlines, semantic HTML
- **Smooth Animations** — card hover effects, drawer slide transitions, modal pop-in, badge pop

## CRUD Operations

| Operation | Entity   | Action                        |
| --------- | -------- | ----------------------------- |
| Create    | Product  | Add a new product via modal   |
| Create    | Cart     | Add product to shopping cart  |
| Read      | Product  | Browse/search/filter products |
| Read      | Cart     | View cart items and total     |
| Update    | Product  | Edit product details          |
| Update    | Cart     | Change item quantity in cart   |
| Delete    | Product  | Remove a product entirely     |
| Delete    | Cart     | Remove item or clear cart     |

## Folder Structure

```
assignment1/
├── backend/
│   ├── app.py                 # aiohttp server entry point
│   ├── requirements.txt       # Python dependencies
│   ├── models/
│   │   └── database.py        # SQLite schema, seed logic, DB connection
│   └── routes/
│       ├── products.py        # Product CRUD API endpoints
│       └── cart.py            # Cart CRUD API endpoints
├── frontend/
│   ├── index.html             # Single HTML entry point
│   ├── .npmrc                 # npm registry config
│   ├── package.json           # Node dependencies and scripts
│   ├── vite.config.js         # Vite build config
│   └── src/
│       ├── main.jsx           # React entry point
│       ├── App.jsx            # Root component with state management
│       ├── App.css            # Global styles and CSS reset
│       ├── services/
│       │   └── api.js         # API client with fetch wrapper
│       ├── hooks/
│       │   ├── useProducts.js # Product state and CRUD logic
│       │   ├── useCart.js     # Cart state and CRUD logic
│       │   └── useToast.js   # Toast notification state
│       └── components/
│           ├── Header.jsx/css         # Top navigation with cart badge
│           ├── SearchBar.jsx/css      # Product search input
│           ├── CategoryFilter.jsx/css # Category pill buttons
│           ├── ProductGrid.jsx/css    # Responsive product grid
│           ├── ProductCard.jsx/css    # Individual product card
│           ├── CartDrawer.jsx/css     # Slide-in cart panel
│           ├── CartItem.jsx/css       # Cart line item with controls
│           ├── ProductModal.jsx/css   # Add/Edit product form dialog
│           └── Toast.jsx/css          # Notification toasts
├── seed_data.json             # Initial product data (12 items)
├── database_export.sql        # SQLite database export
└── README.md                  # This file
```

## Getting Started

### Prerequisites

- Python 3.9+
- Node.js 18+

### Backend

```bash
cd backend
pip install -r requirements.txt
python app.py
```

The API server starts at `http://localhost:8080`. On first run it automatically creates the SQLite database and seeds it with 12 products from `seed_data.json`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The development server starts at `http://localhost:5173`.

## Challenges Overcome

Building a fully async Python backend with aiohttp required careful handling of database connections using context managers to avoid connection leaks. Implementing the cart drawer as a slide-in panel needed precise CSS transitions combined with React state to handle open/close animations smoothly without layout shifts. Ensuring proper stock validation across the cart and product management flows required coordinating frontend and backend validation — the backend enforces stock limits while the frontend provides immediate feedback. Achieving accessibility across all interactive components (modals, drawers, quantity buttons) required attention to focus management, ARIA attributes, and keyboard navigation patterns.
