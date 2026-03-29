import "./Toast.css";

export default function Toast({ toasts }) {
  return (
    <div className="toast-container" role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast--${toast.type}`}>
          <span className="toast__icon">{toast.type === "success" ? "✓" : "✕"}</span>
          <span className="toast__message">{toast.message}</span>
        </div>
      ))}
    </div>
  );
}
