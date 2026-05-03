import "./Toast.css";
import type { ToastMessage } from "../types";

interface ToastProps {
  toasts: ToastMessage[];
}

export default function Toast({ toasts }: ToastProps) {
  return (
    <div className="toast-container" role="status" aria-live="polite">
      {toasts.map((toast) => (
        <div key={toast.id} className={`toast toast--${toast.type}`}>
          <span className="toast__icon">{toast.type === "success" ? <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><polyline points="2 7 5.5 10.5 12 3.5"/></svg> : <svg width="12" height="12" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>}</span>
          <span className="toast__message">{toast.message}</span>
        </div>
      ))}
    </div>
  );
}
