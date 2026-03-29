import "./CartItem.css";

export default function CartItem({ item, onUpdate, onRemove }) {
  return (
    <li className="cart-item">
      <img className="cart-item__img" src={item.image_url} alt={item.name} />
      <div className="cart-item__info">
        <h4 className="cart-item__name">{item.name}</h4>
        <span className="cart-item__price">${(item.price * item.quantity).toFixed(2)}</span>
        <div className="cart-item__controls">
          <button
            className="cart-item__qty-btn"
            onClick={() => onUpdate(item.id, item.quantity - 1)}
            disabled={item.quantity <= 1}
            aria-label={`Decrease quantity of ${item.name}`}
          >
            −
          </button>
          <span className="cart-item__qty" aria-label={`Quantity: ${item.quantity}`}>{item.quantity}</span>
          <button
            className="cart-item__qty-btn"
            onClick={() => onUpdate(item.id, item.quantity + 1)}
            disabled={item.quantity >= item.stock}
            aria-label={`Increase quantity of ${item.name}`}
          >
            +
          </button>
        </div>
      </div>
      <button
        className="cart-item__remove"
        onClick={() => onRemove(item.id)}
        aria-label={`Remove ${item.name} from cart`}
      >
        ✕
      </button>
    </li>
  );
}
