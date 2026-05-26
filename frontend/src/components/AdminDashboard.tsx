import { useMemo, useState } from "react";
import CartDrawer from "./CartDrawer";
import Header from "./Header";
import UserGrid from "./UserGrid";
import EditUserModal from "./EditUserModal";
import Toast from "./Toast";
import useToast from "../hooks/useToast";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import type { CartItem, User } from "../types";

interface AdminDashboardProps {
  logoutFunc: () => void;
}

export default function AdminDashboard({ logoutFunc }: AdminDashboardProps) {
  const [cartOpen, setCartOpen] = useState<boolean>(false);
  const [cartItems, setCartItems] = useState<CartItem[]>([]);
  const [selectedUsername, setSelectedUsername] = useState<string | null>(null);
  const [profileOpen, setProfileOpen] = useState(false);
  const { toasts, addToast } = useToast();
  const { auth } = useAuth();

  const cartTotal = useMemo(() => {
    return cartItems.reduce((sum, item) => sum + item.price * item.quantity, 0);
  }, [cartItems]);

  const handleViewCart = async (user: User) => {
    try {
      const userCart = await userApi.getCart(user.id, auth.token);
      setCartItems(userCart);
      setSelectedUsername(user.username);
      setCartOpen(true);
    } catch (error: unknown) {
      addToast(error instanceof Error ? error.message : "Failed to load user cart", "error");
    }
  };

  const onCartDrawClose = () => {
    setCartOpen(false);
    //This is done to ensure that we do not set the username back until the draw is actually closed
    setTimeout(() => setSelectedUsername(null), 400);
  }

  return (
    <div>
      <Header
        onLogout={logoutFunc}
        cartCount={0}
        onCartClick={() => {}}
        onProfileClick={() => setProfileOpen(true)}
      />
      <main style={{ padding: "2rem" }}>
        <UserGrid onViewCart={handleViewCart} addToast={addToast} />
        <CartDrawer
          open={cartOpen}
          cartItems={cartItems}
          cartTotal={cartTotal}
          onClose={onCartDrawClose}
          selectedUsername={selectedUsername}
          addToast={addToast}
        />
      {profileOpen && auth.user && auth.userId && auth.role && (
          <EditUserModal
            user={{ id: auth.userId, username: auth.user, role: auth.role as "admin" | "user" }}
            onClose={() => setProfileOpen(false)}
            onSaved={() => setProfileOpen(false)}
            addToast={addToast}
          />
        )}
      <Toast toasts={toasts} />
      </main>
    </div>
  );
}
