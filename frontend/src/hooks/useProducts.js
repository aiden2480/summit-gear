import { useState, useEffect, useCallback } from "react";
import { productApi, categoryApi } from "../services/api";

export default function useProducts(addToast) {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState("All");
  const [searchQuery, setSearchQuery] = useState("");
  const [loading, setLoading] = useState(true);

  const fetchProducts = useCallback(async () => {
    try {
      setLoading(true);
      const data = await productApi.getAll(selectedCategory, searchQuery);
      setProducts(data);
    } catch {
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
      /* categories are non-critical */
    }
  }, []);

  const refreshStock = useCallback(async () => {
    try {
      const data = await productApi.getAll(selectedCategory, searchQuery);
      setProducts(data);
    } catch {
      /* silent fail on stock refresh */
    }
  }, [selectedCategory, searchQuery]);

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  return {
    products,
    categories,
    selectedCategory,
    setSelectedCategory,
    searchQuery,
    setSearchQuery,
    loading,
    refreshStock,
  };
}
