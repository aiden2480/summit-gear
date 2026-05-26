import type { User } from "../types";
import "./Avatar.css";

interface AvatarProps {
  user: User;
  size?: "sm" | "md" | "lg";
}

function hashString(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = (h * 31 + s.charCodeAt(i)) | 0;
  }
  return Math.abs(h);
}

function gradientFor(id: string): string {
  const h = hashString(id);
  const hue1 = h % 360;
  const hue2 = (hue1 + 40 + (h >> 8) % 60) % 360;
  return `linear-gradient(135deg, hsl(${hue1}, 65%, 45%), hsl(${hue2}, 70%, 30%))`;
}

export default function Avatar({ user, size = "md" }: AvatarProps) {
  const initial = (user.username || "?").charAt(0).toUpperCase();
  const style = user.avatar ? undefined : { background: gradientFor(user.id) };

  return (
    <div className={`avatar avatar--${size}`} style={style} aria-hidden={user.avatar ? "true" : undefined}>
      {user.avatar
        ? <img src={user.avatar} alt={`${user.username}'s profile picture`} />
        : initial}
    </div>
  );
}
