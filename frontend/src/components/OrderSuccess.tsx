import "./OrderSuccess.css";

interface OrderSuccessProps {
  orderId: string;
  onClose: () => void;
}

export default function OrderSuccess({ orderId, onClose }: OrderSuccessProps) {
  return (
    <>
      <div className="order-overlay" onClick={onClose} aria-hidden="true" />
      <div className="order-modal" role="dialog" aria-modal="true" aria-label="Order successful">
        <div className="order-modal__content">
          <div className="order-modal__truck">
            <img src="/pickup_truck.svg" alt="Delivery truck animation" aria-hidden="true" />
          </div>

          <h1 className="order-modal__title">Order Confirmed!</h1>

          <p className="order-modal__message">Your gear is on the way</p>

          <div className="order-modal__order-id">
            <span className="order-modal__label">Order ID:</span>
            <span className="order-modal__id">{orderId}</span>
          </div>

          <button className="btn btn--primary order-modal__button" onClick={onClose}>
            Continue Shopping
          </button>
        </div>
      </div>
    </>
  );
}
