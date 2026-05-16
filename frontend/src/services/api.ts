import { CartItem, User } from "../types"

const API_BASE = "http://localhost:8080/api";

async function request<T>(url: string, token: string | null, options: RequestInit = {}): Promise<T> {
  const headers = new Headers();
  if (token) {
    headers.append("Authorization", `Bearer ${token}`);
  }

  const res = await fetch(`${API_BASE}${url}`, { headers, ...options });

  if (!res.ok) {
    if (res.status === 401) {
      window.dispatchEvent(new CustomEvent("auth:unauthorized"));
    }
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }

  return res.json() as Promise<T>;
}

const get = <T>(url: string, token: string | null = null) => request<T>(url, token);
const post = <T>(url: string, data: unknown, token: string | null = null) => request<T>(url, token, { method: "POST", body: JSON.stringify(data) });
const put = <T>(url: string, data: unknown, token: string | null = null) => request<T>(url, token, { method: "PUT", body: JSON.stringify(data) });
const del = <T>(url: string, token: string | null = null) => request<T>(url, token, { method: "DELETE" });

export const productApi = {
  getAll: (category?: string, search?: string) => {
    const params = new URLSearchParams();

    if (category && category !== "All") {
      params.append("category", category);
    }

    if (search) {
      params.append("search", search);
    }

    const query = params.toString();
    return get<import("../types").Product[]>(query ? `/products?${query}` : "/products");
  },
};

export const cartApi = {
  getAll: (token: string | null = null) => get<CartItem[]>("/cart", token),
  add: (productId: number, quantity = 1, token: string | null) => post<CartItem>("/cart", { product_id: productId, quantity }, token),
  update: (id: number, quantity: number, token: string | null) => put<CartItem>(`/cart/${id}`, { quantity }, token),
  remove: (id: number, token: string | null) => del<{ message: string }>(`/cart/${id}`, token),
  clear: (token: string | null) => del<{ message: string }>("/cart", token),
  checkout: (token: string | null) => post<{ status: string; message: string }>("/checkout", {}, token),
};

export const categoryApi = {
  getAll: () => get<string[]>("/categories"),
};

export const userApi = {
  getAll: (token : string | null = null) => get<User[]>("/users", token),
  getCart: (username : string, token: string | null = null) => get<CartItem[]>(`/users/cart/${username}`, token),
}
