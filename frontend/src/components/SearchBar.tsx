import { useState, useEffect } from "react";
import "./SearchBar.css";

interface SearchBarProps {
  value: string;
  onChange: (value: string) => void;
}

/** Search input that waits for the user to stop typing before notifying the parent. */
export default function SearchBar({ value, onChange }: SearchBarProps) {
  const [internalValue, setInternalValue] = useState(value);
  const delay = 300;

  useEffect(() => {
    setInternalValue(value);
  }, [value]);

  // debounce emitting changes to parent
  useEffect(() => {
    const id = setTimeout(() => {
      if (internalValue !== value) {
        onChange(internalValue);
      }
    }, delay);
    return () => clearTimeout(id);
  }, [internalValue, onChange, value]);

  return (
    <div className="search-bar">
      <span className="search-bar__icon" aria-hidden="true">
        <img src="/magnifying_glass.svg" alt="" className="search-bar__icon-img" />
      </span>
      <input
        className="search-bar__input"
        type="text"
        placeholder="Search gear..."
        value={internalValue}
        onChange={(e) => setInternalValue(e.target.value)}
        aria-label="Search gear"
      />
      {internalValue && (
        <button
          className="search-bar__clear"
          onClick={() => {
            setInternalValue("");
            onChange("");
          }}
          aria-label="Clear search"
        >
          <svg width="12" height="12" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round"><line x1="1" y1="1" x2="13" y2="13"/><line x1="13" y1="1" x2="1" y2="13"/></svg>
        </button>
      )}
    </div>
  );
}
