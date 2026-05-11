import React from "react";
import "./Grid.css";

export interface GridProps {
  empty : boolean
  loading: boolean;
  error: string | null;
  children: React.ReactNode;
  emptyIcon?: string;
  emptyTitle?: string;
  emptyDescription?: string;
}

export default function Grid({
  empty,
  loading,
  error,
  children,
  emptyIcon = "/package.svg",
  emptyTitle = "No items found",
  emptyDescription = "Try adjusting your search or filter criteria.",
}: GridProps) {
  if (loading) {
    return (
      <div className="grid__loading" role="status">
        <span>Loading...</span>
      </div>
    );
  }

  if (error) {
    return (
      <div className="grid__empty" role="alert">
        <span className="grid__empty-icon" aria-hidden="true">
          <img src={emptyIcon} alt="" className="grid__empty-img" />
        </span>
        <h3>Error</h3>
        <p>{error}</p>
      </div>
    );
  }

  if (empty) {
    return (
      <div className="grid__empty">
        <span className="grid__empty-icon" aria-hidden="true">
          <img src={emptyIcon} alt="" className="grid__empty-img" />
        </span>
        <h3>{emptyTitle}</h3>
        <p>{emptyDescription}</p>
      </div>
    );
  }

  return (
    <div className="grid" role="list">
      {children}
    </div>
  );
}
