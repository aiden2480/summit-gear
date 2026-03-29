import "./ProductCard.css";

export default function ProductCard({ product, onAddToCart, onEdit, onDelete }) {
  const outOfStock = product.stock <= 0;

  return (
    <article className="product-card" tabIndex={0}>
      <div className="product-card__img-wrapper">
        <img
          className="product-card__img"
          src={product.image_url}
          alt={product.name}
          loading="lazy"
        />
        {outOfStock && <div className="product-card__badge product-card__badge--out">Out of Stock</div>}
        {!outOfStock && product.stock <= 5 && (
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
              onClick={() => onAddToCart(product.id)}
              disabled={outOfStock}
              aria-label={`Add ${product.name} to cart`}
            >
              Add to Cart
            </button>
          </div>
        </div>
      </div>
    </article>
  );
}
