import Header from "./Header";

interface AdminDashboardProps { logoutFunc : () => void }

export default function AdminDashboard({ logoutFunc } : AdminDashboardProps) {
  return (
    <div>
      <Header onLogout={logoutFunc} cartCount={0} onCartClick={() => {}}/>
    </div>
  )
}
