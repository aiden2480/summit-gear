import { createContext, useContext, useState, useEffect } from "react";
import type { User } from "../types";

interface AuthState {
  user: string | null;
  userId: string | null;
  token: string | null;
  role: string | null;
  avatar: string | null;
}

interface AuthContextType {
  auth: AuthState;
  getLoggedInUser: () => User;
  login: (user: string, token: string, role: string, userId: string, avatar?: string | null) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [auth, setAuth] = useState<AuthState>({
    user: localStorage.getItem("user"),
    userId: localStorage.getItem("userId"),
    token: localStorage.getItem("token"),
    role: localStorage.getItem("role"),
    avatar: localStorage.getItem("avatar"),
  });

  const getLoggedInUser = (): User => {
    return {
      id: auth.userId!,
      username: auth.user!,
      role: auth.role as "admin" | "user",
      avatar: auth.avatar ?? null,
    };
  }

  const login = (user: string, token: string, role: string, userId: string, avatar: string | null = null) => {
    localStorage.setItem("user", user);
    localStorage.setItem("userId", userId);
    localStorage.setItem("token", token);
    localStorage.setItem("role", role);
    if (avatar) localStorage.setItem("avatar", avatar);
    else localStorage.removeItem("avatar");
    setAuth({ user, userId, token, role, avatar });
  };

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("userId");
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    localStorage.removeItem("avatar");
    setAuth({ user: null, userId: null, token: null, role: null, avatar: null });
  };

  useEffect(() => {
    window.addEventListener("auth:unauthorized", logout);
    return () => window.removeEventListener("auth:unauthorized", logout);
  }, []);

  return (
    <AuthContext value={{ auth, getLoggedInUser, login, logout }}>
      {children}
    </AuthContext>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
