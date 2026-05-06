import { useCallback, useState } from "react";
import { BrowserRouter, Routes, Route, Navigate, useNavigate } from "react-router-dom";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import CategoryFilter from "./components/CategoryFilter";
import ProductGrid from "./components/ProductGrid";
import CartDrawer from "./components/CartDrawer";
import Toast from "./components/Toast";
import Login from "./components/Login";
import Register from "./components/Register";
import useToast from "./hooks/useToast";
import useProducts from "./hooks/useProducts";
import useCart from "./hooks/useCart";
import "./shared.css";
import "./App.css";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const user = localStorage.getItem("user");
  return !user ? <Navigate to="/login" replace /> : <>{children}</>;
};

const ProtectedLoginRoute = ({ children }: { children: React.ReactNode }) => {
  const user = localStorage.getItem("user");
  return user ? <Navigate to="/" replace /> : <>{children}</>;
};

function NoMatch() {
  return (
    <div style={{ padding: 20 }}>
      <h2>404: Page Not Found</h2>
    </div>
  );
}

function ShopPage() {
  const navigate = useNavigate();
  const { toasts, addToast } = useToast();
  const {
    products,
    categories,
    selectedCategory,
    setSelectedCategory,
    searchQuery,
    setSearchQuery,
    loading,
    error,
    refreshStock,
  } = useProducts(addToast);
  const { cartItems, cartCount, cartTotal, addToCart, updateQuantity, removeItem, clearCart, fetchCart } = useCart(addToast);

  const [cartOpen, setCartOpen] = useState(false);

  const handleAddToCart = useCallback(async (productId: number) => {
    await addToCart(productId);
  }, [addToCart]);

  const handleCheckoutSuccess = async () => {
    await fetchCart();
    await refreshStock();
  };

  const handleLogout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    navigate("/login", { replace: true });
  };

  return (
    <div className="app">
      <Header cartCount={cartCount} onCartClick={() => setCartOpen(true)} onLogout={handleLogout} />

      <main className="main">
        <div className="main__toolbar">
          <SearchBar value={searchQuery} onChange={setSearchQuery} />
          <CategoryFilter categories={categories} selected={selectedCategory} onSelect={setSelectedCategory} />
        </div>
        <ProductGrid
          products={products}
          loading={loading}
          error={error}
          onAddToCart={handleAddToCart}
        />
      </main>

      <CartDrawer
        open={cartOpen}
        cartItems={cartItems}
        cartTotal={cartTotal}
        onClose={() => setCartOpen(false)}
        onUpdate={updateQuantity}
        onRemove={removeItem}
        onClear={clearCart}
        onCheckoutSuccess={handleCheckoutSuccess}
        addToast={addToast}
      />

      <Toast toasts={toasts} />
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><ShopPage /></ProtectedRoute>} />
        <Route path="/login" element={<ProtectedLoginRoute><Login /></ProtectedLoginRoute>} />
        <Route path="/register" element={<ProtectedLoginRoute><Register /></ProtectedLoginRoute>} />
        <Route path="*" element={<NoMatch />} />
      </Routes>
    </BrowserRouter>
  );
}

