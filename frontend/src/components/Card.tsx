import React from "react";
import "./Card.css";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

export default function Card({ children, className = "" }: CardProps) {
  return (
    <article className={`card ${className}`.trim()} tabIndex={0}>
      {children}
    </article>
  );
}
