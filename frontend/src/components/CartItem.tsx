import "./CartItem.css";
import type { CartItem as CartItemType } from "../types";

interface CartItemProps {
  item: CartItemType;
  onUpdate: (itemId: number, quantity: number) => void | Promise<void>;
  onRemove: (itemId: number) => void | Promise<void>;
}

export default function CartItem({ item, onUpdate, onRemove }: CartItemProps) {
  return (
    <li className="cart-item">
      <img className="cart-item__img" src={item.image_url} alt={item.name} />
      <div className="cart-item__info">
        <h4 className="cart-item__name">{item.name}</h4>
        <span className="cart-item__price">${(item.price * item.quantity).toFixed(2)}</span>
        <div className="cart-item__controls">
          <button
            className="cart-item__qty-btn"
            onClick={() => void onUpdate(item.id, item.quantity - 1)}
            disabled={item.quantity <= 1}
            aria-label={`Decrease quantity of ${item.name}`}
          >
            −
          </button>
          <span className="cart-item__qty" aria-label={`Quantity: ${item.quantity}`}>{item.quantity}</span>
          <button
            className="cart-item__qty-btn"
            onClick={() => void onUpdate(item.id, item.quantity + 1)}
            disabled={item.quantity >= item.stock}
            aria-label={`Increase quantity of ${item.name}`}
          >
            +
          </button>
        </div>
      </div>
      <button
        className="cart-item__remove"
        onClick={() => void onRemove(item.id)}
        aria-label={`Remove ${item.name} from cart`}
      >
        <svg width="12" height="12" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>
      </button>
    </li>
  );
}
