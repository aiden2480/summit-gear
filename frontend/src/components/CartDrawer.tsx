import { useState, useEffect, useCallback } from "react";
import "./CartDrawer.css";
import CartItem from "./CartItem";
import OrderSuccess from "./OrderSuccess";
import { cartApi } from "../services/api";
import type { CartItem as CartItemType, ToastType } from "../types";

interface CartDrawerProps {
  open: boolean;
  cartItems: CartItemType[];
  cartTotal: number;
  onClose: () => void;
  onUpdate: (itemId: number, quantity: number) => void | Promise<void>;
  onRemove: (itemId: number) => void | Promise<void>;
  onClear: () => void | Promise<void>;
  onCheckoutSuccess?: () => void | Promise<void>;
  addToast: (message: string, type?: ToastType) => void;
}

function getErrorMessage(error: unknown) {
  return error instanceof Error ? error.message : "Checkout failed. Please try again.";
}

export default function CartDrawer({ open, cartItems, cartTotal, onClose, onUpdate, onRemove, onClear, onCheckoutSuccess, addToast }: CartDrawerProps) {
  const [orderPlaced, setOrderPlaced] = useState(false);
  const [orderId, setOrderId] = useState("");

  const handleOrderClose = useCallback(() => {
    setOrderPlaced(false);
    onClose();
  }, [onClose]);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        if (orderPlaced) {
          handleOrderClose();
        } else if (open) {
          onClose();
        }
      }
    };

    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [open, orderPlaced, onClose, handleOrderClose]);

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
        await onCheckoutSuccess();
      }
    } catch (error: unknown) {
      addToast(getErrorMessage(error), "error");
    }
  };

  if (orderPlaced) {
    return <OrderSuccess orderId={orderId} onClose={handleOrderClose} />;
  }

  return (
    <>
      <div className={`cart-overlay${open ? " cart-overlay--visible" : ""}`} onClick={onClose} aria-hidden="true" />
      <aside
        className={`cart-drawer${open ? " cart-drawer--open" : ""}`}
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
                <CartItem key={item.id} item={item} onUpdate={onUpdate} onRemove={onRemove} />
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
              onClick={() => void handleCheckout()}
            >
              Checkout
            </button>
            <button className="btn btn--text" onClick={() => void onClear()}>
              Clear Cart
            </button>
          </div>
        )}
      </aside>
    </>
  );
}
