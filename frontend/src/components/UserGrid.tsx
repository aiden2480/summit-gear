import Grid from "./Grid";
import UserCard from "./UserCard";
import type { User } from "../types";
import { useEffect, useState } from "react";
import { userApi } from "../services/api";
import { useAuth } from "../context/AuthContext";

export default function UserGrid() {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const { auth } = useAuth();

  useEffect(() => {
    async function fetchUsers() {
      setLoading(true);
      setError(null);
      try {
        const gottenUsers = await userApi.getAll(auth.token);
        setUsers(gottenUsers);
      }
      catch (e) {
        console.log(e);
        setError("Unable to load users.");
      }
      finally {
        setLoading(false);
      }
    }

    fetchUsers();
  }, [auth.token]);

  const handleEditUser = (username: string) => {
    // TODO: Implement edit user
    console.log("Edit user:", username);
  };

  const handleDeleteUser = (username: string) => {
    // TODO: Implement delete user
    console.log("Delete user:", username);
  };

  return (
    <Grid
      empty={users.length === 0}
      loading={loading}
      error={error}
      emptyTitle="No users found"
      emptyDescription="No users have been created yet."
    >
      {users.map((user, index) => (
        <div key={user.username} style={{ animationDelay: `${index * 0.05}s` }}>
          <UserCard user={user} onEdit={handleEditUser} onDelete={handleDeleteUser} />
        </div>
      ))}
    </Grid>
  );
}
