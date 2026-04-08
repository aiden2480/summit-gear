import "./SearchBar.css";

export default function SearchBar({ value, onChange }) {
  return (
    <div className="search-bar">
      <span className="search-bar__icon" aria-hidden="true">
        <img src="/magnifying_glass.svg" alt="" className="search-bar__icon-img" />
      </span>
      <input
        className="search-bar__input"
        type="text"
        placeholder="Search gear..."
        value={value}
        onChange={(e) => onChange(e.target.value)}
        aria-label="Search gear"
      />
      {value && (
        <button
          className="search-bar__clear"
          onClick={() => onChange("")}
          aria-label="Clear search"
        >
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>
        </button>
      )}
    </div>
  );
}
