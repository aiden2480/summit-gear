import "./CartDrawer.css";
import CartItem from "./CartItem";

export default function CartDrawer({ open, cartItems, cartTotal, onClose, onUpdate, onRemove, onClear }) {
  return (
    <>
      <div className={`cart-overlay ${open ? "cart-overlay--visible" : ""}`} onClick={onClose} aria-hidden="true" />
      <aside
        className={`cart-drawer ${open ? "cart-drawer--open" : ""}`}
        role="dialog"
        aria-label="Shopping cart"
        aria-modal="true"
      >
        <div className="cart-drawer__header">
          <h2 className="cart-drawer__title">Your Cart</h2>
          <button className="cart-drawer__close" onClick={onClose} aria-label="Close cart">
            ✕
          </button>
        </div>

        <div className="cart-drawer__body">
          {cartItems.length === 0 ? (
            <div className="cart-drawer__empty">
              <span aria-hidden="true">🛒</span>
              <p>Your cart is empty</p>
              <button className="btn btn--primary" onClick={onClose}>
                Continue Shopping
              </button>
            </div>
          ) : (
            <ul className="cart-drawer__list">
              {cartItems.map((item) => (
                <CartItem
                  key={item.id}
                  item={item}
                  onUpdate={onUpdate}
                  onRemove={onRemove}
                />
              ))}
            </ul>
          )}
        </div>

        {cartItems.length > 0 && (
          <div className="cart-drawer__footer">
            <div className="cart-drawer__total">
              <span>Total</span>
              <span className="cart-drawer__total-price">${cartTotal.toFixed(2)}</span>
            </div>
            <button className="btn btn--primary cart-drawer__checkout">
              Checkout
            </button>
            <button className="btn btn--text" onClick={onClear}>
              Clear Cart
            </button>
          </div>
        )}
      </aside>
    </>
  );
}
