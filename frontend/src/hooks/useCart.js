import { useState, useEffect, useCallback } from "react";
import { cartApi } from "../services/api";

export default function useCart(addToast) {
  const [cartItems, setCartItems] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchCart = useCallback(async () => {
    try {
      setLoading(true);
      const data = await cartApi.getAll();
      setCartItems(data);
    } catch {
      addToast("Failed to load cart", "error");
    } finally {
      setLoading(false);
    }
  }, [addToast]);

  useEffect(() => {
    fetchCart();
  }, [fetchCart]);

  const addToCart = async (productId) => {
    try {
      await cartApi.add(productId, 1);
      await fetchCart();
      addToast("Added to cart!");
    } catch (err) {
      addToast(err.message || "Failed to add to cart", "error");
    }
  };

  const updateQuantity = async (itemId, quantity) => {
    try {
      await cartApi.update(itemId, quantity);
      await fetchCart();
    } catch (err) {
      addToast(err.message || "Failed to update quantity", "error");
    }
  };

  const removeItem = async (itemId) => {
    try {
      await cartApi.remove(itemId);
      await fetchCart();
      addToast("Removed from cart");
    } catch (err) {
      addToast(err.message || "Failed to remove item", "error");
    }
  };

  const clearCart = async () => {
    try {
      await cartApi.clear();
      setCartItems([]);
      addToast("Cart cleared");
    } catch {
      addToast("Failed to clear cart", "error");
    }
  };

  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const cartTotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return { cartItems, cartCount, cartTotal, loading, addToCart, updateQuantity, removeItem, clearCart, fetchCart };
}
