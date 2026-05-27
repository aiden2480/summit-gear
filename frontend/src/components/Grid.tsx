import React from "react";
import "./Grid.css";

export interface GridProps {
  className?: string;
  empty: boolean;
  loading: boolean;
  error: string | null;
  children: React.ReactNode;
  loadingText: string;
  errorTitle?: string;
  emptyIcon?: string;
  emptyClassName?: string;
  emptyTitle?: string;
  emptyDescription?: string;
}

export default function Grid({
  className = "",
  empty,
  loading,
  error,
  children,
  loadingText,
  errorTitle = "Error",
  emptyIcon = "/package.svg",
  emptyClassName = "",
  emptyTitle = "No items found",
  emptyDescription = "Try adjusting your search or filter criteria.",
}: GridProps) {
  if (loading) {
    return (
      <div className="grid__loading" role="status">
        <span className="grid__spinner" aria-hidden="true" />
        <span>{loadingText}</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className={`grid__empty ${emptyClassName}`.trim()} role="alert">
        <span className="grid__empty-icon" aria-hidden="true">
          <img src={emptyIcon} alt="" className="grid__empty-img" />
        </span>
        <h3>{errorTitle}</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (empty) {
    return (
      <div className={`grid__empty ${emptyClassName}`.trim()}>
        <span className="grid__empty-icon" aria-hidden="true">
          <img src={emptyIcon} alt="" className="grid__empty-img" />
        </span>
        <h3>{emptyTitle}</h3>
        <p>{emptyDescription}</p>
      </div>
    );
  }

  return (
    <div className={`grid ${className}`.trim()} role="list">
      {children}
    </div>
  );
}
