import { useCallback, useState } from "react";
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

type AuthView = "login" | "register";

function ShopPage() {
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
    window.location.reload();
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

function App() {
  const [user, setUser] = useState<string | null>(localStorage.getItem("user"));
  const [authView, setAuthView] = useState<AuthView>("login");

  const handleLogin = (username: string, token: string) => {
    setUser(username);
    localStorage.setItem("user", username);
    localStorage.setItem("token", token);
  };

  if (!user) {
    return authView === "login" ? (
      <Login onLogin={handleLogin} onSwitch={() => setAuthView("register")} />
    ) : (
      <Register onLogin={handleLogin} onSwitch={() => setAuthView("login")} />
    );
  }

  return <ShopPage />;
}

export default App;

