import Card from "./Card";
import "./ProductCard.css";
import type { Product } from "../types";

interface ProductCardProps {
  product: Product;
  onAddToCart: (productId: number) => void | Promise<void>;
}

export default function ProductCard({ product, onAddToCart }: ProductCardProps) {
  const outOfStock = product.stock <= 0;

  return (
    <Card className={`product-card${outOfStock ? " product-card--out-of-stock" : ""}`}>
      <div className="product-card__img-wrapper">
        <img
          className="product-card__img"
          src={product.image_url}
          alt={product.name}
          loading="lazy"
        />
        {outOfStock && <div className="product-card__badge product-card__badge--out">Out of Stock</div>}
        {!outOfStock && product.stock <= 10 && (
          <div className="product-card__badge product-card__badge--low">Only {product.stock} left</div>
        )}
      </div>
      <div className="product-card__body">
        <span className="product-card__category">{product.category}</span>
        <h3 className="product-card__name">{product.name}</h3>
        <p className="product-card__desc">{product.description}</p>
        <div className="product-card__footer">
          <span className="product-card__price">${product.price.toFixed(2)}</span>
          <div className="product-card__actions">
            <button
              className="btn btn--primary"
              onClick={() => void onAddToCart(product.id)}
              disabled={outOfStock}
              aria-label={`Add ${product.name} to cart`}
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </Card>
  );
}
