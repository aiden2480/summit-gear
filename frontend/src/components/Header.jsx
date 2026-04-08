import "./Header.css";

export default function Header({ cartCount, onCartClick }) {
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
          <button className="btn btn--cart" onClick={onCartClick} aria-label={`Shopping cart with ${cartCount} items`}>
            <span className="btn__cart-icon" aria-hidden="true">
              <img src="/backpack.svg" alt="" className="btn__cart-img" />
            </span>
            Cart
            {cartCount > 0 && <span className="header__badge">{cartCount}</span>}
          </button>
        </nav>
      </div>
    </header>
  );
}
