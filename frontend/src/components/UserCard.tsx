import "./UserCard.css";
import Card from "./Card";
import Avatar from "./Avatar";
import type { User } from "../types";

interface UserCardProps {
  user: User;
  onEdit?: (userId: string) => void;
  onDelete?: (userId: string) => void;
  openCart: (user: User) => void;
}


export default function UserCard({ user, onEdit, onDelete, openCart }: UserCardProps) {
  return (
    <Card className="user-card">
      <div className="user-card__header">
        <Avatar user={user} size="md" />
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
              onEdit(user.id);
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
              onDelete(user.id);
            }}
            aria-label={`Delete ${user.username}`}
          >
            Delete
          </button>
        )}
        {user.role != "admin" && (
          <button
            type="button"
            className="btn btn--info btn--small"
            onClick={() => {
              openCart(user);
            }}
          >
            View Cart
          </button>
        )}
        
      </div>
    </Card>
  );
}
