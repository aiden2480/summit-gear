import { useMemo, useState } from "react";
import CartDrawer from "./CartDrawer";
import Header from "./Header";
import UserGrid from "./UserGrid";
import Toast from "./Toast";
import useToast from "../hooks/useToast";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import type { CartItem } from "../types";

interface AdminDashboardProps {
  logoutFunc: () => void;
}

export default function AdminDashboard({ logoutFunc }: AdminDashboardProps) {
  const [cartOpen, setCartOpen] = useState<boolean>(false);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const { toasts, addToast } = useToast();
  const { auth } = useAuth();

  const cartTotal = useMemo(() => {
    return cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }, [cartItems]);

  const handleViewCart = async (username: string) => {
    try {
      const userCart = await userApi.getCart(username, auth.token);
      setCartItems(userCart);
      setCartOpen(true);
    } catch (error: unknown) {
      addToast(error instanceof Error ? error.message : "Failed to load user cart", "error");
    }
  };

  return (
    <div>
      <Header onLogout={logoutFunc} cartCount={0} onCartClick={() => {}} />
      <main style={{ padding: "2rem" }}>
        <UserGrid onViewCart={handleViewCart} />
        <CartDrawer
          open={cartOpen}
          cartItems={cartItems}
          cartTotal={cartTotal}
          onClose={() => setCartOpen(false)}
          addToast={addToast}
        />
      <Toast toasts={toasts} />
      </main>
    </div>
  );
}
