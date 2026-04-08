const API_BASE = "http://localhost:8080/api";

// Centralised API client — all fetch calls go through request() which handles
// JSON headers, error extraction, and throws on non-2xx responses.
async function request(url, options = {}) {
  const res = await fetch(`${API_BASE}${url}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || `Request failed with status ${res.status}`);
  }
  return res.json();
}

// CRUD operations expressed as HTTP request methods
const get = (url) => request(url);
const post = (url, data) => request(url, { method: "POST", body: JSON.stringify(data) });
const put = (url, data) => request(url, { method: "PUT", body: JSON.stringify(data) });
const del = (url) => request(url, { method: "DELETE" });

export const productApi = {
  getAll: (category, search) => {
    const params = new URLSearchParams();
    if (category && category !== "All") params.append("category", category);
    if (search) params.append("search", search);
    return get(`/products?${params.toString()}`);
  },
};

export const cartApi = {
  getAll: () => get("/cart"),
  add: (productId, quantity = 1) => post("/cart", { product_id: productId, quantity }),
  update: (id, quantity) => put(`/cart/${id}`, { quantity }),
  remove: (id) => del(`/cart/${id}`),
  clear: () => del("/cart"),
  checkout: () => post("/checkout", {}),
};

export const categoryApi = {
  getAll: () => get("/categories"),
};
