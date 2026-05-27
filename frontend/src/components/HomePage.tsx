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
      { /* Conditionally render the home page depending on whether the user's role is an admin or not, so that we show each user the correct home page */ }
      { auth.role === "admin" ?
          <AdminDashboard logoutFunc={handleLogout} />
        : 
          <ShopPage logoutFunc={handleLogout} />
      }
    </>
  )
}
