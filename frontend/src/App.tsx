import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./components/Login";
import Register from "./components/Register";
import { useAuth } from "./context/AuthContext";
import "./shared.css";
import "./App.css";
import HomePage from "./components/HomePage";

const ProtectedRoute = ({ children }: { children: React.ReactNode }) => {
  const { auth } = useAuth();
  return !auth.user ? <Navigate to="/login" replace /> : <>{children}</>;
};

const ProtectedLoginRoute = ({ children }: { children: React.ReactNode }) => {
  const { auth } = useAuth();
  return auth.user ? <Navigate to="/" replace /> : <>{children}</>;
};

function NoMatch() {
  return (
    <div style={{ padding: 20 }}>
      <h2>404: Page Not Found</h2>
    </div>
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<ProtectedRoute><HomePage /></ProtectedRoute>} />
        <Route path="/login" element={<ProtectedLoginRoute><Login /></ProtectedLoginRoute>} />
        <Route path="/register" element={<ProtectedLoginRoute><Register /></ProtectedLoginRoute>} />
        <Route path="*" element={<NoMatch />} />
      </Routes>
    </BrowserRouter>
  );
}

