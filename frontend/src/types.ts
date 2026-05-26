export interface Product {
  id: number;
  name: string;
  description: string;
  price: number;
  image_url: string;
  category: string;
  stock: number;
}

export interface CartItem {
  id: number;
  product_id: number;
  quantity: number;
  name: string;
  price: number;
  image_url: string;
  stock: number;
  user_id: string;
}

export interface User {
  id: string,
  username: string;
  role: "admin" | "user";
  avatar: string | null;
}

export type ToastType = "success" | "error";

export interface ToastMessage {
  id: number;
  message: string;
  type: ToastType;
}

export interface UpdateUserPayload {
  email?: string;
  password?: string;
  role?: "user" | "admin";
  avatar?: File;
  removeAvatar?: boolean;
}
