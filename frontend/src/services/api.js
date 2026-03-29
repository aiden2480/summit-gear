const API_BASE = "http://localhost:8080/api";

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

export const productApi = {
  getAll: (category, search) => {
    const params = new URLSearchParams();
    if (category && category !== "All") params.append("category", category);
    if (search) params.append("search", search);
    const qs = params.toString();
    return request(`/products${qs ? `?${qs}` : ""}`);
  },
  getById: (id) => request(`/products/${id}`),
  create: (data) => request("/products", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) => request(`/products/${id}`, { method: "PUT", body: JSON.stringify(data) }),
  delete: (id) => request(`/products/${id}`, { method: "DELETE" }),
};

export const cartApi = {
  getAll: () => request("/cart"),
  add: (productId, quantity = 1) => request("/cart", { method: "POST", body: JSON.stringify({ product_id: productId, quantity }) }),
  update: (id, quantity) => request(`/cart/${id}`, { method: "PUT", body: JSON.stringify({ quantity }) }),
  remove: (id) => request(`/cart/${id}`, { method: "DELETE" }),
  clear: () => request("/cart", { method: "DELETE" }),
};

export const categoryApi = {
  getAll: () => request("/categories"),
};
