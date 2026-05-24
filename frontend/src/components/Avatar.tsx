import type { User } from "../types";
import "./Avatar.css";

interface AvatarProps {
  user: Pick<User, "username" | "avatar">;
  size?: "sm" | "md" | "lg";
}

export default function Avatar({ user, size = "md" }: AvatarProps) {
  const initial = (user.username || "?").charAt(0).toUpperCase();

  return (
    <div className={`avatar avatar--${size}`} aria-hidden={user.avatar ? "true" : undefined}>
      {user.avatar
        ? <img src={user.avatar} alt={`${user.username}'s profile picture`} />
        : initial}
    </div>
  );
}
