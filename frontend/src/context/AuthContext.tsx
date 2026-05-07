import { createContext, useContext, useState } from "react";

interface AuthState {
  user: string | null;
  token: string | null;
  role: string | null;
}

interface AuthContextType {
  auth: AuthState;
  login: (user: string, token: string, role: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [auth, setAuth] = useState<AuthState>({
    user: localStorage.getItem("user"),
    token: localStorage.getItem("token"),
    role: localStorage.getItem("role"),
  });

  const login = (user: string, token: string, role: string) => {
    localStorage.setItem("user", user);
    localStorage.setItem("token", token);
    localStorage.setItem("role", role);
    setAuth({ user, token, role });
  };

  const logout = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setAuth({ user: null, token: null, role: null });
  };

  return (
    <AuthContext.Provider value={{ auth, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth(): AuthContextType {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
