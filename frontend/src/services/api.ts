import { CartItem } from "../types"

const API_BASE = "http://localhost:8080/api";

async function request<T>(url: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }

  return res.json() as Promise<T>;
}

const get = <T>(url: string) => request<T>(url);
const post = <T>(url: string, data: unknown) => request<T>(url, { method: "POST", body: JSON.stringify(data) });
const put = <T>(url: string, data: unknown) => request<T>(url, { method: "PUT", body: JSON.stringify(data) });
const del = <T>(url: string) => request<T>(url, { method: "DELETE" });

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
  getAll: () => get<CartItem[]>("/cart"),
  add: (productId: number, quantity = 1) => post<CartItem>("/cart", { product_id: productId, quantity }),
  update: (id: number, quantity: number) => put<CartItem>(`/cart/${id}`, { quantity }),
  remove: (id: number) => del<{ message: string }>(`/cart/${id}`),
  clear: () => del<{ message: string }>("/cart"),
  checkout: () => post<{ status: string; message: string }>("/checkout", {}),
};

export const categoryApi = {
  getAll: () => get<string[]>("/categories"),
};
