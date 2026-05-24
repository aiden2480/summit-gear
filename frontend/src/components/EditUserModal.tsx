import { useState } from "react";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import type { User, ToastType } from "../types";
import "./UserCard.css";
import "./Header.css";
import "./EditUserModal.css";

interface EditUserModalProps {
  user: User;
  mode: "self" | "admin";
  onClose: () => void;
  onSaved: (updated: User) => void;
  addToast: (message: string, type?: ToastType) => void;
}

export default function EditUserModal({ user, mode, onClose, onSaved, addToast }: EditUserModalProps) {
  const { auth, login } = useAuth();
  const [email, setEmail] = useState(user.username);
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"user" | "admin">(user.role);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const isSelfTarget = auth.user === user.username;
  const showRoleField = mode === "admin" && !isSelfTarget;

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError(null);

    const trimmedEmail = email.trim();
    const payload: { email?: string; password?: string; role?: "user" | "admin" } = {};

    if (trimmedEmail !== user.username) {
      payload.email = trimmedEmail;
    }

    if (password.length > 0) {
      if (password.length < 8) {
        setError("Password must be at least 8 characters");
        return;
      }
      payload.password = password;
    }

    if (showRoleField && role !== user.role) {
      payload.role = role;
    }

    if (Object.keys(payload).length === 0) {
      setError("No changes to save");
      return;
    }

    setSubmitting(true);
    try {
      const updated = mode === "self"
        ? await userApi.updateSelf(payload, auth.token)
        : await userApi.updateUser(user.id, payload, auth.token);
      addToast("User updated successfully", "success");
      if (isSelfTarget && updated.username !== auth.user) {
        login(updated.username, auth.token!, updated.role, updated.id);
      }
      onSaved(updated);
      onClose();
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Failed to update user";
      setError(msg);
      addToast(msg, "error");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <>
      <div className="modal-overlay" onClick={onClose} aria-hidden="true" />
      <div className="modal" role="dialog" aria-modal="true" aria-label="Edit user">
        <h2 className="modal__title">{mode === "self" ? "Edit Profile" : "Edit User"}</h2>
        <p className="modal__subtitle">
          {mode === "self" ? "Update your account details" : `Editing ${user.username}`}
        </p>

        <form className="modal__form" onSubmit={handleSubmit}>
          <div className="modal__field">
            <label htmlFor="edit-user-email">Email</label>
            <input
              id="edit-user-email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              autoComplete="email"
              required
            />
          </div>

          <div className="modal__field">
            <label htmlFor="edit-user-password">New Password</label>
            <input
              id="edit-user-password"
              type="password"
              placeholder="Leave blank to keep unchanged"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="new-password"
            />
            <span className="modal__hint">Minimum 8 characters</span>
          </div>

          {showRoleField && (
            <div className="modal__field">
              <label htmlFor="edit-user-role">Role</label>
              <select
                id="edit-user-role"
                value={role}
                onChange={(e) => setRole(e.target.value as "user" | "admin")}
              >
                <option value="user">user</option>
                <option value="admin">admin</option>
              </select>
            </div>
          )}

          {error && <div className="modal__error">{error}</div>}

          <div className="modal__actions">
            <button type="button" className="btn btn--logout" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn--success" disabled={submitting}>
              {submitting ? "Saving..." : "Save Changes"}
            </button>
          </div>
        </form>
      </div>
    </>
  );
}
