import { useState, useCallback } from "react";
import Header from "./components/Header";
import SearchBar from "./components/SearchBar";
import CategoryFilter from "./components/CategoryFilter";
import ProductGrid from "./components/ProductGrid";
import CartDrawer from "./components/CartDrawer";
import ProductModal from "./components/ProductModal";
import Toast from "./components/Toast";
import useToast from "./hooks/useToast";
import useProducts from "./hooks/useProducts";
import useCart from "./hooks/useCart";
import "./App.css";

function App() {
  const { toasts, addToast } = useToast();
  const {
    products, categories, selectedCategory, setSelectedCategory,
    searchQuery, setSearchQuery, loading,
    createProduct, updateProduct, deleteProduct,
  } = useProducts(addToast);
  const { cartItems, cartCount, cartTotal, addToCart, updateQuantity, removeItem, clearCart } = useCart(addToast);

  const [cartOpen, setCartOpen] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);

  const handleAddProduct = useCallback(() => {
    setEditingProduct(null);
    setModalOpen(true);
  }, []);

  const handleEditProduct = useCallback((product) => {
    setEditingProduct(product);
    setModalOpen(true);
  }, []);

  const handleDeleteProduct = useCallback(async (id) => {
    if (window.confirm("Are you sure you want to delete this product?")) {
      try {
        await deleteProduct(id);
      } catch {
        addToast("Failed to delete product", "error");
      }
    }
  }, [deleteProduct, addToast]);

  const handleSaveProduct = useCallback(async (data) => {
    if (editingProduct) {
      await updateProduct(editingProduct.id, data);
    } else {
      await createProduct(data);
    }
  }, [editingProduct, updateProduct, createProduct]);

  const handleAddToCart = useCallback(async (productId) => {
    await addToCart(productId);
    setCartOpen(true);
  }, [addToCart]);

  return (
    <div className="app">
      <Header cartCount={cartCount} onCartClick={() => setCartOpen(true)} onAddProduct={handleAddProduct} />

      <main className="main">
        <div className="main__toolbar">
          <SearchBar value={searchQuery} onChange={setSearchQuery} />
          <CategoryFilter categories={categories} selected={selectedCategory} onSelect={setSelectedCategory} />
        </div>
        <ProductGrid
          products={products}
          loading={loading}
          onAddToCart={handleAddToCart}
          onEdit={handleEditProduct}
          onDelete={handleDeleteProduct}
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
      />

      <ProductModal
        open={modalOpen}
        product={editingProduct}
        onClose={() => setModalOpen(false)}
        onSave={handleSaveProduct}
      />

      <Toast toasts={toasts} />
    </div>
  );
}

export default App;
