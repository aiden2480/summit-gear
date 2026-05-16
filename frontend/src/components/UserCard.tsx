import "./UserCard.css";
import Card from "./Card";
import type { User } from "../types";

interface UserCardProps {
  user: User;
  onEdit: (username: string) => void;
  onDelete: (username: string) => void;
  openCart: (username: string) => void;
}


export default function UserCard({ user, onEdit, onDelete, openCart }: UserCardProps) {
  return (
    <Card className="user-card">
      <div className="user-card__header">
        <div className="user-card__avatar">{user.username.charAt(0).toUpperCase()}</div>
        <div className="user-card__badge" data-role={user.role}>
          {user.role}
        </div>
      </div>
      <div className="user-card__body">
        <h3 className="user-card__username">{user.username}</h3>
      </div>
      <div className="user-card__footer">
        {onEdit && (
          <button
            type="button"
            className="btn btn--success btn--small"
            onClick={() => {
              onEdit(user.username);
            }}
            aria-label={`Edit ${user.username}`}
          >
            Edit
          </button>
        )}
        {onDelete && (
          <button
            type="button"
            className="btn btn--danger btn--small"
            onClick={() => {
              onDelete(user.username);
            }}
            aria-label={`Delete ${user.username}`}
          >
            Delete
          </button>
        )}
        <button
          type="button"
          className="btn btn--small"
          onClick={() => {
            openCart(user.username);
          }}
        >
          View Cart
        </button>
      </div>
    </Card>
  );
}
