import ProductCard from "./ProductCard";
import "./ProductGrid.css";

export default function ProductGrid({ products, loading, onAddToCart }) {
  if (loading) {
    return (
      <div className="product-grid__loading" role="status">
        <div className="spinner" aria-hidden="true"></div>
        <span>Loading products...</span>
      </div>
    );
  }

  if (products.length === 0) {
    return (
      <div className="product-grid__empty">
        <span className="product-grid__empty-icon" aria-hidden="true">📦</span>
        <h3>No products found</h3>
        <p>Try adjusting your search or filter criteria.</p>
      </div>
    );
  }

  return (
    <div className="product-grid" role="list">
      {products.map((product, i) => (
        <div key={product.id} role="listitem" style={{ animationDelay: `${i * 0.05}s` }}>
          <ProductCard
            product={product}
            onAddToCart={onAddToCart}
          />
        </div>
      ))}
    </div>
  );
}
