"use client";

import React from "react";
import { CATEGORIES } from "@/lib/constants";

export interface CategoryBarProps {
  activeCategory?: string;
  onSelectCategory?: (slug: string) => void;
  className?: string;
}

export const CATEGORY_TABS = [
  { id: "all", name: "All Products", icon: "⚡" },
  { id: "top-picks", name: "Top Picks", icon: "🏆" },
  ...CATEGORIES.map((cat) => ({
    id: cat.slug,
    name: cat.name,
    icon: cat.icon,
  })),
];

/**
 * CategoryBar is now unified directly within the Navbar component
 * to ensure a single, connected frosted glass container and unified hover spotlight.
 */
export const CategoryBar: React.FC<CategoryBarProps> = () => {
  return null;
};

export default CategoryBar;
