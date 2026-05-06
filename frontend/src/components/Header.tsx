import "./Header.css";

interface HeaderProps {
  cartCount: number;
  onCartClick: () => void;
  onLogout?: () => void;
}

export default function Header({ cartCount, onCartClick, onLogout }: HeaderProps) {
  const user = localStorage.getItem("user");
  const role = localStorage.getItem("role");

  return (
    <header className="header">
      <div className="header__inner">
        <div className="header__brand">
          <span className="header__logo" aria-hidden="true">
            <img src="/sunrise.svg" alt="" className="header__logo-img" />
          </span>
          <h1 className="header__title">Summit Gear</h1>
        </div>
        <nav className="header__actions">
          {user && (
            <span className="header__user">
              👤 {user}
              {role === "admin" && <span className="header__admin-badge">Admin</span>}
            </span>
          )}
          <button className="btn btn--cart" onClick={onCartClick} aria-label={`Shopping cart with ${cartCount} items`}>
            <span className="btn__cart-icon" aria-hidden="true">
              <img src="/backpack.svg" alt="" className="btn__cart-img" />
            </span>
            Cart
            {cartCount > 0 && <span className="header__badge">{cartCount}</span>}
          </button>
          {onLogout && (
            <button className="btn btn--logout" onClick={onLogout}>
              Sign Out
            </button>
          )}
        </nav>
      </div>
    </header>
  );
}
