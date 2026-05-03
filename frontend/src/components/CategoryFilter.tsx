import "./CategoryFilter.css";

interface CategoryFilterProps {
  categories: string[];
  selected: string;
  onSelect: (category: string) => void;
}

export default function CategoryFilter({ categories, selected, onSelect }: CategoryFilterProps) {
  return (
    <div className="category-filter" role="tablist" aria-label="Filter by category">
      {categories.map((category) => (
        <button
          key={category}
          role="tab"
          aria-selected={selected === category}
          className={`category-filter__btn ${selected === category ? "category-filter__btn--active" : ""}`}
          onClick={() => onSelect(category)}
        >
          {category}
        </button>
      ))}
    </div>
  );
}
