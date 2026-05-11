import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import AdminDashboard from "./AdminDashboard";
import ShopPage from "./ShopPage";

export default function HomePage() {
  const { auth, logout } = useAuth();
  const navigate = useNavigate();

  function handleLogout() {
    logout();
    navigate("/login", { replace: true });
  };

  return (
    <>
      { auth.role === "admin" ?
          <AdminDashboard logoutFunc={handleLogout} />
        : 
          <ShopPage logoutFunc={handleLogout} />
      }
    </>
  )
}
