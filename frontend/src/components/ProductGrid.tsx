import ProductCard from "./ProductCard";
import "./ProductGrid.css";
import type { Product } from "../types";

interface ProductGridProps {
  products: Product[];
  loading: boolean;
  error: string | null;
  onAddToCart: (productId: number) => void | Promise<void>;
}

export default function ProductGrid({ products, loading, error, onAddToCart }: ProductGridProps) {
  if (loading) {
    return (
      <div className="product-grid__loading" role="status">
        <div className="spinner" aria-hidden="true"></div>
        <span>Loading products...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="product-grid__empty" role="alert">
        <span className="product-grid__empty-icon" aria-hidden="true">
          <img src="/package.svg" alt="" className="product-grid__empty-img" />
        </span>
        <h3>Connection Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="product-grid__empty">
        <span className="product-grid__empty-icon" aria-hidden="true">
          <img src="/package.svg" alt="" className="product-grid__empty-img" />
        </span>
        <h3>No products found</h3>
        <p>Try adjusting your search or filter criteria.</p>
      </div>
    );
  }

  return (
    <div className="product-grid" role="list">
      {products.map((product, index) => (
        <div key={product.id} role="listitem" style={{ animationDelay: `${index * 0.05}s` }}>
          <ProductCard product={product} onAddToCart={onAddToCart} />
        </div>
      ))}
    </div>
  );
}
