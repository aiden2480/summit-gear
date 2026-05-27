import { useRef, useState, useEffect } from "react";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import Avatar from "./Avatar";
import type { User, ToastType, UpdateUserPayload } from "../types";
import "./UserCard.css";
import "./Header.css";
import "./EditUserModal.css";

interface EditUserModalProps {
  user?: User;
  onClose: () => void;
  onSaved: (updated: User) => void;
  addToast: (message: string, type?: ToastType) => void;
}

const ALLOWED_AVATAR_TYPES = ["image/png", "image/jpeg"];
const MAX_AVATAR_BYTES = 2 * 1024 * 1024;

export default function EditUserModal({ user: userProp, onClose, onSaved, addToast }: EditUserModalProps) {
  const { auth, getLoggedInUser, login } = useAuth();
  const initialUser = userProp ?? getLoggedInUser();

  const [user] = useState<User>(initialUser);
  const [email, setEmail] = useState(initialUser.username);
  const [password, setPassword] = useState("");
  const [role, setRole] = useState<"user" | "admin">(initialUser.role);
  const [submitting, setSubmitting] = useState(false);
  const [pendingFile, setPendingFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(initialUser.avatar ?? null);
  const [removeAvatar, setRemoveAvatar] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const isSelfTarget = auth.userId === user.id;
  const showRoleField = auth.role === "admin" && !isSelfTarget;

  useEffect(() => {
    function handleKeyDown(e: KeyboardEvent) {
      if (e.key === "Escape") {
        onClose();
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  function handleFileChange(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    e.target.value = "";
    if (!file) return;

    if (!ALLOWED_AVATAR_TYPES.includes(file.type)) {
      addToast("Profile picture must be a PNG or JPEG image", "error");
      return;
    }
    if (file.size > MAX_AVATAR_BYTES) {
      addToast("Profile picture must be 2 MB or smaller", "error");
      return;
    }

    setPendingFile(file);
    setRemoveAvatar(false);
    setPreviewUrl(URL.createObjectURL(file));
  }

  function handleRemoveAvatar() {
    setPendingFile(null);
    setPreviewUrl(null);
    setRemoveAvatar(true);
  }

  async function handleSubmit(e: React.SubmitEvent) {
    e.preventDefault();

    const trimmedEmail = email.trim();
    const payload: UpdateUserPayload = {};

    if (password.length > 0 && password.length < 8) {
      addToast("Password must be at least 8 characters", "error");
      return;
    }

    if (password.length > 0)
      payload.password = password;
    if (trimmedEmail !== user.username)
      payload.email = trimmedEmail;
    if (showRoleField && role !== user.role)
      payload.role = role;
    if (pendingFile)
      payload.avatar = pendingFile;
    if (removeAvatar)
      payload.removeAvatar = removeAvatar;

    if (Object.keys(payload).length === 0) {
      addToast("No changes to save", "error");
      return;
    }

    setSubmitting(true);

    try {
      const updatedUser = isSelfTarget
        ? await userApi.updateSelf(payload, auth.token)
        : await userApi.updateUser(user.id, payload, auth.token);

      addToast("Saved successfully", "success");

      // If we are editing ourself, call login again so we can update the header icon
      if (isSelfTarget) {
        login(updatedUser.username, auth.token!, updatedUser.role, updatedUser.id, updatedUser.avatar);
      }
      
      onSaved(updatedUser);
      onClose();
    } catch (e: unknown) {
      addToast(e instanceof Error ? e.message : "Failed to update user", "error");
    } finally {
      setSubmitting(false);
    }
  }

  const avatarPreviewUser = { ...user, avatar: previewUrl };
  const hasAvatar = previewUrl !== null;

  return (
    <>
      <div className="modal-overlay" onClick={onClose} aria-hidden="true" />
      <div className="modal" role="dialog" aria-modal="true" aria-label="Edit user">
        <h2 className="modal__title">{isSelfTarget ? "Edit Profile" : "Edit User"}</h2>

        <div className="modal__avatar-section">
          <Avatar user={avatarPreviewUser} size="lg" />
          <div className="modal__avatar-actions">
            <input
              ref={fileInputRef}
              type="file"
              accept="image/png,image/jpeg"
              onChange={handleFileChange}
              style={{ display: "none" }}
            />
            <div className="modal__avatar-buttons">
              <button
                type="button"
                className="btn btn--success btn--small"
                onClick={() => fileInputRef.current?.click()}
                disabled={submitting}
              >
                Upload photo
              </button>
              {hasAvatar && (
                <button
                  type="button"
                  className="btn btn--danger btn--small"
                  onClick={handleRemoveAvatar}
                  disabled={submitting}
                >
                  Remove photo
                </button>
              )}
            </div>
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
                <option value="user">User</option>
                <option value="admin">Admin</option>
              </select>
            </div>
          )}

          <div className="modal__actions">
            <button type="button" className="btn btn--logout" onClick={onClose} disabled={submitting}>
              Cancel
            </button>
            <button type="submit" className="btn btn--success" disabled={submitting}>
              Save Changes
            </button>
          </div>
        </form>
      </div>
    </>
  );
}
