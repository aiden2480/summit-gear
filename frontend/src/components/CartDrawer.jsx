import { useState, useEffect } from "react";
import "./CartDrawer.css";
import CartItem from "./CartItem";
import OrderSuccess from "./OrderSuccess";
import { cartApi } from "../services/api";

export default function CartDrawer({ open, cartItems, cartTotal, onClose, onUpdate, onRemove, onClear, onCheckoutSuccess, addToast }) {
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState("");

  // Close drawer on Escape key press
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        if (orderPlaced) {
          handleOrderClose();
        } else if (open) {
          onClose();
        }
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [open, orderPlaced, onClose]);

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
      addToast(error.message || "Checkout failed. Please try again.", "error");
    }
  };

  const handleOrderClose = () => {
    setOrderPlaced(false);
    onClose();
  };

  if (orderPlaced) {
    return <OrderSuccess orderId={orderId} onClose={handleOrderClose} />;
  }

  return (
    <>
      <div className={`cart-overlay${open ? ' cart-overlay--visible' : ''}`} onClick={onClose} aria-hidden="true" />
      <aside
        className={`cart-drawer${open ? ' cart-drawer--open' : ''}`}
        role="dialog"
        aria-label="Shopping cart"
        aria-modal={open}
        aria-hidden={!open}
      >
        <div className="cart-drawer__header">
          <h2 className="cart-drawer__title">Your Cart</h2>
          <button className="btn--close" onClick={onClose} aria-label="Close cart">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>
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
