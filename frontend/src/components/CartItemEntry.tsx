import "./CartItem.css";
import type { CartItem } from "../types";

interface CartItemEntryProps {
  item: CartItem;
  onUpdate?: (itemId: number, quantity: number) => void | Promise<void>;
  onRemove?: (itemId: number) => void | Promise<void>;
}

export default function CartItemEntry({ item, onUpdate, onRemove }: CartItemEntryProps) {
  //If any action is unavailable, then we should view the cart items in a read-only mode
``` would make more sense if the user cannot edit or update items then the cart items are readonly i.e admin users
  const isReadOnly = !onUpdate || !onRemove;

  return (
    <li className={`cart-item${isReadOnly ? " cart-item--readonly" : ""}`}>
      <img className="cart-item__img" src={item.image_url} alt={item.name} />
      <div className="cart-item__info">
        <h4 className="cart-item__name">{item.name}</h4>
        <span className="cart-item__price">${(item.price * item.quantity).toFixed(2)}</span>
          <div className="cart-item__controls">
          {onUpdate && 
            <button
              className="cart-item__qty-btn"
              onClick={() => void onUpdate(item.id, item.quantity - 1)}
              disabled={item.quantity <= 1}
              aria-label={`Decrease quantity of ${item.name}`}
            >
              −
            </button>}
            <span className="cart-item__qty" aria-label={`Quantity: ${item.quantity}`}>{(!isReadOnly ? "" : "Quantity: ") + item.quantity}</span>
          {onUpdate && 
            <button
              className="cart-item__qty-btn"
              onClick={() => void onUpdate(item.id, item.quantity + 1)}
              disabled={item.quantity >= item.stock}
              aria-label={`Increase quantity of ${item.name}`}
            >
              +
            </button>}
          </div>
      </div>
      {onRemove && (
        <button
          className="cart-item__remove"
          onClick={() => void onRemove(item.id)}
          aria-label={`Remove ${item.name} from cart`}
        >
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>
        </button>
      )}
    </li>
  );
}
