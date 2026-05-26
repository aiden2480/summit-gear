import Grid from "./Grid";
import ProductCard from "./ProductCard";
import type { Product } from "../types";

interface ProductGridProps {
  products: Product[];
  loading: boolean;
  error: string | null;
  onAddToCart: (productId: number) => void | Promise<void>;
}

export default function ProductGrid({ products, loading, error, onAddToCart }: ProductGridProps) {
  return (
    <Grid
      className="product-grid"
      loading={loading}
      error={error}
      empty={products.length === 0}
      loadingText="Loading products..."
      errorTitle="Connection Error"
      emptyClassName="product-grid__empty"
      emptyTitle="No products found"
      emptyDescription="Try adjusting your search or filter criteria."
    >
      {products.map((product, index) => (
        <div key={product.id} role="listitem" style={{ animationDelay: `${index * 0.05}s` }}>
          <ProductCard product={product} onAddToCart={onAddToCart} />
        </div>
      ))}
    </Grid>
  );
}
