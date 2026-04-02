import "./SearchBar.css";

export default function SearchBar({ value, onChange }) {
  return (
    <div className="search-bar">
      <span className="search-bar__icon" aria-hidden="true">🔍</span>
      <input
        className="search-bar__input"
        type="search"
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
          ✕
        </button>
      )}
    </div>
  );
}
