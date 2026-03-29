import "./CategoryFilter.css";

export default function CategoryFilter({ categories, selected, onSelect }) {
  return (
    <div className="category-filter" role="tablist" aria-label="Filter by category">
      {categories.map((cat) => (
        <button
          key={cat}
          role="tab"
          aria-selected={selected === cat}
          className={`category-filter__btn ${selected === cat ? "category-filter__btn--active" : ""}`}
          onClick={() => onSelect(cat)}
        >
          {cat}
        </button>
      ))}
    </div>
  );
}
