import { useCallback, useState } from "react";
import Header from "./Header";
import SearchBar from "./SearchBar";
import CategoryFilter from "./CategoryFilter";
import ProductGrid from "./ProductGrid";
import CartDrawer from "./CartDrawer";
import Toast from "./Toast";
import EditUserModal from "./EditUserModal";
import { useAuth } from "../context/AuthContext";
import useToast from "../hooks/useToast";
import useProducts from "../hooks/useProducts";
import useCart from "../hooks/useCart";
import "../shared.css";
import "../App.css";

interface ShopPageProps { logoutFunc : () => void }

export default function ShopPage({ logoutFunc } : ShopPageProps) {
  const { toasts, addToast } = useToast();
  const { auth } = useAuth();
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
  const [profileOpen, setProfileOpen] = useState(false);

  const handleAddToCart = useCallback(async (productId: number) => {
    await addToCart(productId);
  }, [addToCart]);

  const handleCheckoutSuccess = async () => {
    await fetchCart();
    await refreshStock();
  };

  return (
    <div className="app">
      <Header
        cartCount={cartCount}
        onCartClick={() => setCartOpen(true)}
        onLogout={logoutFunc}
        onProfileClick={() => setProfileOpen(true)}
      />

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

      {profileOpen && auth.user && auth.userId && auth.role && (
        <EditUserModal
          user={{ id: auth.userId, username: auth.user, role: auth.role as "admin" | "user" }}
          isAdminMode={false}
          onClose={() => setProfileOpen(false)}
          onSaved={() => setProfileOpen(false)}
          addToast={addToast}
        />
      )}

      <Toast toasts={toasts} />
    </div>
  );
}
