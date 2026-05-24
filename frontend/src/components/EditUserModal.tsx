import { useRef, useState } from "react";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import Avatar from "./Avatar";
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

const ALLOWED_AVATAR_TYPES = ["image/png", "image/jpeg"];
const MAX_AVATAR_BYTES = 2 * 1024 * 1024;

export default function EditUserModal({ user: initialUser, mode, onClose, onSaved, addToast }: EditUserModalProps) {
  const { auth, login, setAvatar } = useAuth();
  const [user, setUser] = useState<User>(initialUser);
  const [email, setEmail] = useState(initialUser.username);
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"user" | "admin">(initialUser.role);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [avatarBusy, setAvatarBusy] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const isSelfTarget = auth.user === user.username;
  const showRoleField = mode === "admin" && !isSelfTarget;

  function extractErrorMessage(e: unknown, fallback: string) {
    let msg = e instanceof Error ? e.message : fallback;
    try {
      const parsed = JSON.parse(msg);
      if (parsed && typeof parsed.error === "string") {
        msg = parsed.error;
      }
    } catch {
      // not JSON, use raw message
    }
    return msg;
  }

  function applyAvatarUpdate(updated: User) {
    setUser(updated);
    onSaved(updated);
    if (isSelfTarget) {
      setAvatar(updated.avatar);
    }
  }

  async function handleAvatarChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;

    if (!ALLOWED_AVATAR_TYPES.includes(file.type)) {
      setError("Profile picture must be a PNG or JPEG image");
      addToast("Profile picture must be a PNG or JPEG image", "error");
      return;
    }

    if (file.size > MAX_AVATAR_BYTES) {
      setError("Profile picture must be 2 MB or smaller");
      addToast("Profile picture must be 2 MB or smaller", "error");
      return;
    }

    setError(null);
    setAvatarBusy(true);
    try {
      const updated = mode === "self"
        ? await userApi.uploadSelfAvatar(file, auth.token)
        : await userApi.uploadUserAvatar(user.id, file, auth.token);
      applyAvatarUpdate(updated);
      addToast("Profile picture updated", "success");
    } catch (err) {
      const msg = extractErrorMessage(err, "Failed to upload profile picture");
      setError(msg);
      addToast(msg, "error");
    } finally {
      setAvatarBusy(false);
    }
  }

  async function handleAvatarRemove() {
    setError(null);
    setAvatarBusy(true);
    try {
      const updated = mode === "self"
        ? await userApi.deleteSelfAvatar(auth.token)
        : await userApi.deleteUserAvatar(user.id, auth.token);
      applyAvatarUpdate(updated);
      addToast("Profile picture removed", "success");
    } catch (err) {
      const msg = extractErrorMessage(err, "Failed to remove profile picture");
      setError(msg);
      addToast(msg, "error");
    } finally {
      setAvatarBusy(false);
    }
  }

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
        login(updated.username, auth.token!, updated.role, updated.id, updated.avatar);
      }
      onSaved(updated);
      onClose();
    } catch (e: unknown) {
      const msg = extractErrorMessage(e, "Failed to update user");
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

        <div className="modal__avatar-section">
          <Avatar user={user} size="lg" />
          <div className="modal__avatar-actions">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg"
              onChange={handleAvatarChange}
              style={{ display: "none" }}
            />
            <button
              type="button"
              className="btn btn--success btn--small"
              onClick={() => fileInputRef.current?.click()}
              disabled={avatarBusy}
            >
              {avatarBusy ? "Uploading..." : user.avatar ? "Change photo" : "Upload photo"}
            </button>
            {user.avatar && (
              <button
                type="button"
                className="btn btn--danger btn--small"
                onClick={handleAvatarRemove}
                disabled={avatarBusy}
              >
                Remove photo
              </button>
            )}
            <span className="modal__hint">PNG or JPEG, up to 2 MB</span>
          </div>
        </div>

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
