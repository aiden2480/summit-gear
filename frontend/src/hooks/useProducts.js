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

  useEffect(() => {
    fetchProducts();
  }, [fetchProducts]);

  useEffect(() => {
    fetchCategories();
  }, [fetchCategories]);

  const createProduct = async (data) => {
    const product = await productApi.create(data);
    await fetchProducts();
    await fetchCategories();
    addToast("Product added!");
    return product;
  };

  const updateProduct = async (id, data) => {
    const product = await productApi.update(id, data);
    await fetchProducts();
    await fetchCategories();
    addToast("Product updated!");
    return product;
  };

  const deleteProduct = async (id) => {
    await productApi.delete(id);
    await fetchProducts();
    await fetchCategories();
    addToast("Product deleted");
  };

  return {
    products,
    categories,
    selectedCategory,
    setSelectedCategory,
    searchQuery,
    setSearchQuery,
    loading,
    createProduct,
    updateProduct,
    deleteProduct,
  };
}
