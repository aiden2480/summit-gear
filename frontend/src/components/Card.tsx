import React from "react";
import "./Card.css";

interface CardProps {
  children: React.ReactNode;
  className?: string;
}

//A base component for user and product card, that contains all of the base logic for a grid card
export default function Card({ children, className = "" }: CardProps) {
  return (
    <article className={`card ${className}`.trim()} tabIndex={0}>
      {children}
    </article>
  );
}
