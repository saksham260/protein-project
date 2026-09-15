"use client";

import React from "react";
import { cn } from "@/lib/utils";

export interface AnimatedSearchButtonProps
  extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  size?: number;
}

export const AnimatedSearchButton: React.FC<AnimatedSearchButtonProps> = ({
  size = 38,
  className,
  ...props
}) => {
  return (
    <button
      type="submit"
      aria-label="Search"
      style={{ width: `${size}px`, height: `${size}px` }}
      className={cn("search-morph-btn", className)}
      {...props}
    >
      <div className="search-morph-canvas">
        <div className="search-morph-circle" />
        <span className="search-morph-handle" />
      </div>
    </button>
  );
};
