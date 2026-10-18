"use client";

import React from "react";
import { CATEGORIES, PRIMARY_CATEGORY_SLUGS } from "@/lib/constants";

export interface CategoryBarProps {
  activeCategory?: string;
  onSelectCategory?: (slug: string) => void;
  className?: string;
}

export const PRIMARY_CATEGORY_TABS = [
  { id: "all", name: "Home", icon: "🏠" },
  { id: "top-picks", name: "Top Picks", icon: "🏆" },
  ...CATEGORIES.filter((cat) => (PRIMARY_CATEGORY_SLUGS as readonly string[]).includes(cat.slug)).map((cat) => ({
    id: cat.slug,
    name: cat.name,
    icon: cat.icon,
  })),
];

export const SECONDARY_CATEGORIES = CATEGORIES.filter(
  (cat) => !(PRIMARY_CATEGORY_SLUGS as readonly string[]).includes(cat.slug)
);

export const CATEGORY_TABS = [
  { id: "all", name: "Home", icon: "🏠" },
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
