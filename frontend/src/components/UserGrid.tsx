import Grid from "./Grid";
import UserCard from "./UserCard";
import EditUserModal from "./EditUserModal";
import ConfirmDialog from "./ConfirmDialog";
import { useCallback, useEffect, useState } from "react";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";
import type { User, ToastType } from "../types";

interface UserGridProps {
  onViewCart: (user: User) => Promise<void>;
  addToast: (message: string, type?: ToastType) => void;
}

export default function UserGrid({ onViewCart, addToast }: UserGridProps) {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<User | null>(null);
  const [deleting, setDeleting] = useState<User | null>(null);
  const [deleteBusy, setDeleteBusy] = useState(false);
  const { auth } = useAuth();

  const fetchUsers = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const gottenUsers = await userApi.getAll(auth.token);
      setUsers(gottenUsers);
    }
    catch (e) {
      console.error(e);
      setError("Unable to load users.");
    }
    finally {
      setLoading(false);
    }
  }, [auth.token]);

  useEffect(() => {
    fetchUsers();
  }, [fetchUsers]);

  function handleEditUser(userId: string) {
    const user = users.find((u) => u.id === userId);
    if (user) setEditing(user);
  }

  function handleDeleteUser(userId: string) {
    const user = users.find((u) => u.id === userId);
    if (user) setDeleting(user);
  }

  async function confirmDelete() {
    if (!deleting) return;
    setDeleteBusy(true);
    try {
      await userApi.delete(deleting.id, auth.token);
      addToast(`Deleted ${deleting.username}`, "success");
      setDeleting(null);
      await fetchUsers();
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Failed to delete user";
      addToast(msg, "error");
    } finally {
      setDeleteBusy(false);
    }
  }

  function handleSaved(updated: User) {
    setUsers((prev) => prev.map((u) => (u.id === updated.id ? updated : u)));
  }

  return (
    <>
      <Grid
        empty={users.length === 0}
        loading={loading}
        error={error}
        emptyTitle="No users found"
        emptyDescription="No users have been created yet."
      >
        {users.map((user, index) => (
          <div key={user.id} style={{ animationDelay: `${index * 0.05}s` }}>
            <UserCard
              user={user}
              onEdit={handleEditUser}
              onDelete={user.id === auth.userId ? undefined : handleDeleteUser}
              openCart={onViewCart}
            />
          </div>
        ))}
      </Grid>

      {editing && (
        <EditUserModal
          user={editing}
          onClose={() => setEditing(null)}
          onSaved={handleSaved}
          addToast={addToast}
        />
      )}

      {deleting && (
        <ConfirmDialog
          title="Delete user?"
          message={`Are you sure you want to delete ${deleting.username}? This action cannot be undone.`}
          confirmLabel="Delete"
          destructive
          busy={deleteBusy}
          onConfirm={confirmDelete}
          onCancel={() => (deleteBusy ? null : setDeleting(null))}
        />
      )}
    </>
  );
}
