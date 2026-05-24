import "./UserCard.css";
import "./Header.css";
import "./EditUserModal.css";

interface ConfirmDialogProps {
  title: string;
  message: string;
  confirmLabel?: string;
  cancelLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
  busy?: boolean;
  destructive?: boolean;
}

export default function ConfirmDialog({
  title,
  message,
  confirmLabel = "Confirm",
  cancelLabel = "Cancel",
  onConfirm,
  onCancel,
  busy = false,
  destructive = false,
}: ConfirmDialogProps) {
  return (
    <>
      <div className="modal-overlay" onClick={onCancel} aria-hidden="true" />
      <div className="modal" role="alertdialog" aria-modal="true" aria-label={title}>
        <h2 className="modal__title">{title}</h2>
        <p className="modal__subtitle">{message}</p>
        <div className="modal__actions">
          <button type="button" className="btn btn--logout" onClick={onCancel} disabled={busy}>
            {cancelLabel}
          </button>
          <button
            type="button"
            className={destructive ? "btn btn--danger" : "btn btn--success"}
            onClick={onConfirm}
            disabled={busy}
          >
            {busy ? "Working..." : confirmLabel}
          </button>
        </div>
      </div>
    </>
  );
}
