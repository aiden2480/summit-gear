import { CartItem, UpdateUserPayload, User } from "../types"

const API_BASE = "http://localhost:8080/api";

export class ApiError extends Error {
  status: number;
  body: unknown;

  constructor(status: number, message: string, body: unknown = null) {
    super(message);
    this.name = "ApiError";
    this.status = status;
    this.body = body;
  }
}

async function parseError(res: Response): Promise<{ message: string; body: unknown }> {
  const text = await res.text();
  if (!text) {
    return { message: `Request failed with status ${res.status}`, body: null };
  }
  try {
    const data = JSON.parse(text);
    const message =
      (data && typeof data.error === "string" && data.error) ||
      (data && typeof data.message === "string" && data.message) ||
      `Request failed with status ${res.status}`;
    return { message, body: data };
  } catch {
    return { message: text, body: text };
  }
}

async function request<T>(url: string, token: string | null, options: RequestInit = {}): Promise<T> {
  const headers = new Headers();
  if (token) {
    headers.append("Authorization", `Bearer ${token}`);
  }
  if (typeof options.body === "string" && !headers.has("Content-Type")) {
    headers.append("Content-Type", "application/json");
  }

  const res = await fetch(`${API_BASE}${url}`, { headers, ...options });

  if (!res.ok) {
    if (res.status === 401) {
      window.dispatchEvent(new CustomEvent("auth:unauthorized"));
    }
    const { message, body } = await parseError(res);
    throw new ApiError(res.status, message, body);
  }

  return res.json() as Promise<T>;
}

const get = <T>(url: string, token: string | null = null) => request<T>(url, token);
const post = <T>(url: string, data: unknown, token: string | null = null) => request<T>(url, token, { method: "POST", body: JSON.stringify(data) });
const put = <T>(url: string, data: unknown, token: string | null = null) => request<T>(url, token, { method: "PUT", body: JSON.stringify(data) });
const del = <T>(url: string, token: string | null = null) => request<T>(url, token, { method: "DELETE" });

const putMultipart = <T>(url: string, formData: FormData, token: string | null = null) =>
  request<T>(url, token, { method: "PUT", body: formData });

export const authApi = {
  login: (username: string, password: string) => {
    const headers = new Headers({ "Content-Type": "application/json" });
    return fetch(`http://localhost:8080/login`, {
      method: "POST",
      headers,
      body: JSON.stringify({ username, password }),
    }).then(async (res) => {
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Request failed with status ${res.status}`);
      }
      return res.json();
    });
  },
  register: (username: string, password: string) => {
    const headers = new Headers({ "Content-Type": "application/json" });
    return fetch(`http://localhost:8080/register`, {
      method: "POST",
      headers,
      body: JSON.stringify({ username, password }),
    }).then(async (res) => {
      if (!res.ok) {
        const text = await res.text();
        throw new Error(text || `Request failed with status ${res.status}`);
      }
      return res.json();
    });
  },
};

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

export interface AuthResponse {
  id: string;
  user: string;
  token: string;
  role: "user" | "admin";
  avatar?: string | null;
}

export interface RegisterResponse {
  user: string;
  role: "user" | "admin";
}

const AUTH_BASE = "http://localhost:8080";

async function authRequest<T>(path: string, body: unknown): Promise<T> {
  const res = await fetch(`${AUTH_BASE}${path}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!res.ok) {
    const { message, body: errBody } = await parseError(res);
    throw new ApiError(res.status, message, errBody);
  }
  return res.json() as Promise<T>;
}

export const authApi = {
  login: (username: string, password: string) =>
    authRequest<AuthResponse>("/login", { username, password }),
  register: (username: string, password: string) =>
    authRequest<RegisterResponse>("/register", { username, password }),
};

export const userApi = {
  getAll: (token : string | null = null) => get<User[]>("/users", token),
  getCart: (userId: string, token: string | null = null) => get<CartItem[]>(`/cart/user/${userId}`, token),
  updateSelf: (payload: UpdateUserPayload, token: string | null = null) => putMultipart<User>("/users/me", buildUpdateForm(payload), token),
  updateUser: (userId: string, payload: UpdateUserPayload, token: string | null = null) => putMultipart<User>(`/users/${userId}`, buildUpdateForm(payload), token),
  delete: (userId: string, token: string | null = null) => del<{ message: string }>(`/users/${userId}`, token),
}

function buildUpdateForm(payload: UpdateUserPayload): FormData {
  const form = new FormData();
  if (payload.email) form.append("email", payload.email);
  if (payload.password) form.append("password", payload.password);
  if (payload.role) form.append("role", payload.role);
  if (payload.avatar) form.append("avatar", payload.avatar, payload.avatar.name);
  if (payload.removeAvatar) form.append("remove_avatar", "true");
  return form;
}
