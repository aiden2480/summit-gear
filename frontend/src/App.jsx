import { useState, useCallback } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import CategoryFilter from "./components/CategoryFilter";
import ProductGrid from "./components/ProductGrid";
import CartDrawer from "./components/CartDrawer";
import Toast from "./components/Toast";
import useToast from "./hooks/useToast";
import useProducts from "./hooks/useProducts";
import useCart from "./hooks/useCart";
import "./shared.css";
import "./App.css";

function App() {
  const { toasts, addToast } = useToast();
  const {
    products, categories, selectedCategory, setSelectedCategory,
    searchQuery, setSearchQuery, loading, error, refreshStock,
  } = useProducts(addToast);
  const { cartItems, cartCount, cartTotal, addToCart, updateQuantity, removeItem, clearCart, fetchCart } = useCart(addToast);

  const [cartOpen, setCartOpen] = useState(false);

  const handleAddToCart = useCallback(async (productId) => {
    await addToCart(productId);
  }, [addToCart]);

  // After checkout, re-fetch cart (now empty) and refresh product stock counts
  const handleCheckoutSuccess = async () => {
    await fetchCart();
    refreshStock();
  };

  return (
    <div className="app">
      <Header cartCount={cartCount} onCartClick={() => setCartOpen(true)} />

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

export default App;
