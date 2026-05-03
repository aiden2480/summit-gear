import { useState, useEffect, useCallback } from "react";
import { productApi, categoryApi } from "../services/api";
import type { Product, ToastType } from "../types";

type AddToast = (message: string, type?: ToastType) => void;

export default function useProducts(addToast: AddToast) {
  const [products, setProducts] = useState<Product[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await productApi.getAll(selectedCategory, searchQuery);
      setProducts(data);
    } catch {
      setError("Unable to connect to the server. Please check that the backend is running.");
      addToast("Failed to load products", "error");
    } finally {
      setLoading(false);
    }
  }, [selectedCategory, searchQuery, addToast]);

  const fetchCategories = useCallback(async () => {
    try {
      const data = await categoryApi.getAll();
      setCategories(["All", ...data]);
    } catch {
      // categories are non-critical
    }
  }, []);

  const refreshStock = useCallback(async () => {
    try {
      const data = await productApi.getAll(selectedCategory, searchQuery);
      setProducts(data);
    } catch {
      // silent fail on stock refresh
    }
  }, [selectedCategory, searchQuery]);

  useEffect(() => {
    void fetchProducts();
  }, [fetchProducts]);

  useEffect(() => {
    void fetchCategories();
  }, [fetchCategories]);

  return {
    products,
    categories,
    selectedCategory,
    setSelectedCategory,
    searchQuery,
    setSearchQuery,
    loading,
    error,
    refreshStock,
  };
}
