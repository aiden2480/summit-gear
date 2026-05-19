import Header from "./Header";
import UserGrid from "./UserGrid";

interface AdminDashboardProps {
  logoutFunc: () => void;
}

export default function AdminDashboard({ logoutFunc }: AdminDashboardProps) {
  return (
    <div>
      <Header onLogout={logoutFunc} cartCount={0} onCartClick={() => {}} />
      <main style={{ padding: "2rem" }}>
        <UserGrid />
      </main>
    </div>
  );
}
