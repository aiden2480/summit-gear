import { useState } from "react";
import "./CartDrawer.css";
import CartItem from "./CartItem";
import OrderSuccess from "./OrderSuccess";
import { cartApi } from "../services/api";

export default function CartDrawer({ open, cartItems, cartTotal, onClose, onUpdate, onRemove, onClear, onCheckoutSuccess }) {
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState("");

  const generateOrderId = () => {
    const timestamp = Date.now().toString(36).toUpperCase();
    const random = Math.random().toString(36).substring(2, 8).toUpperCase();
    return `ORD-${timestamp}-${random}`;
  };

  const handleCheckout = async () => {
    try {
      await cartApi.checkout();
      const newOrderId = generateOrderId();
      setOrderId(newOrderId);
      setOrderPlaced(true);
      if (onCheckoutSuccess) {
        onCheckoutSuccess();
      }
    } catch (error) {
      console.error("Checkout failed:", error);
    }
  };

  const handleOrderClose = () => {
    setOrderPlaced(false);
    onClose();
  };

  if (orderPlaced) {
    return <OrderSuccess orderId={orderId} onClose={handleOrderClose} />;
  }

  if (!open) {
    return null;
  }

  return (
    <>
      <div className="cart-overlay cart-overlay--visible" onClick={onClose} aria-hidden="true" />
      <aside
        className="cart-drawer cart-drawer--open"
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
              <img src="/backpack.svg" alt="" className="cart-drawer__empty-img" aria-hidden="true" />
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
            <button 
              type="button"
              className="btn btn--primary cart-drawer__checkout" 
              onClick={handleCheckout}
            >
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
