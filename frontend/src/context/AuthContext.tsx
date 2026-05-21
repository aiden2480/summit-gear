import { createContext, useContext, useState, useEffect } from "react";

interface AuthState {
  user: string | null;
  userId: string | null;
  token: string | null;
  role: string | null;
}

interface AuthContextType {
  auth: AuthState;
  login: (user: string, token: string, role: string, userId: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [auth, setAuth] = useState<AuthState>({
    user: localStorage.getItem("user"),
    userId: localStorage.getItem("userId"),
    token: localStorage.getItem("token"),
    role: localStorage.getItem("role"),
  });

  const login = (user: string, token: string, role: string, userId: string) => {
    localStorage.setItem("user", user);
    localStorage.setItem("userId", userId);
    localStorage.setItem("token", token);
    localStorage.setItem("role", role);
    setAuth({ user, userId, token, role });
  };

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("userId");
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setAuth({ user: null, userId: null, token: null, role: null });
  };

  useEffect(() => {
    window.addEventListener("auth:unauthorized", logout);
    return () => window.removeEventListener("auth:unauthorized", logout);
  }, []);

  return (
    <AuthContext value={{ auth, login, logout }}>
      {children}
    </AuthContext>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
