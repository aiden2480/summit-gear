import { useState, useEffect, useCallback } from "react";
import { cartApi } from "../services/api";
import type { CartItem, ToastType } from "../types";
import { useAuth } from "../context/AuthContext";

type AddToast = (message: string, type?: ToastType) => void;

export default function useCart(addToast: AddToast) {
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [loading, setLoading] = useState(false);
  const { auth } = useAuth();

  const fetchCart = useCallback(async () => {
    try {
      setLoading(true);
      const data = await cartApi.getAll(auth.token);
      setCartItems(data);
    } catch {
      addToast("Failed to load cart", "error");
    } finally {
      setLoading(false);
    }
  }, [addToast, auth.token]);

  useEffect(() => {
    void fetchCart();
  }, [fetchCart]);

  const addToCart = async (productId: number) => {
    try {
      const existingItem = cartItems.find((item) => item.product_id === productId);
      await cartApi.add(productId, 1, auth.token);
      await fetchCart();

      if (existingItem) {
        addToast(`Updated quantity in cart to ${existingItem.quantity + 1}`);
      } else {
        addToast("Added to cart!");
      }
    } catch (error: unknown) {
      addToast(error instanceof Error ? error.message : "Failed to add to cart", "error");
    }
  };

  const updateQuantity = async (itemId: number, quantity: number) => {
    try {
      await cartApi.update(itemId, quantity, auth.token);
      await fetchCart();
    } catch (error: unknown) {
      addToast(error instanceof Error ? error.message : "Failed to update quantity", "error");
    }
  };

  const removeItem = async (itemId: number) => {
    try {
      await cartApi.remove(itemId, auth.token);
      await fetchCart();
    } catch (error: unknown) {
      addToast(error instanceof Error ? error.message : "Failed to remove item", "error");
    }
  };

  const clearCart = async () => {
    try {
      await cartApi.clear(auth.token);
      await fetchCart();
      addToast("Cart cleared");
    } catch {
      addToast("Failed to clear cart", "error");
    }
  };

  const cartCount = cartItems.reduce((sum, item) => sum + item.quantity, 0);
  const cartTotal = cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);

  return { cartItems, cartCount, cartTotal, loading, addToCart, updateQuantity, removeItem, clearCart, fetchCart };
}
