"use client";

import React, { useState } from "react";
import { CATEGORIES, PROTEIN_TIERS, ALLERGENS_LIST, DIETARY_TAGS_LIST } from "@/lib/constants";
import { Badge } from "@/components/ui/Badge";
import { QueryFilters } from "@/lib/data";
import { cn } from "@/lib/utils";

export interface FilterPanelProps {
  filters: QueryFilters;
  onCategoryChange?: (slug?: string) => void;
  onToggleTier: (tier: string) => void;
  onToggleTag: (tag: string) => void;
  onToggleAllergen: (allergen: string) => void;
  onSetZeroFlagsOnly: (val: boolean) => void;
  onClearFilters: () => void;
  hideCategoryFilter?: boolean;
  className?: string;
}

export const FilterPanel: React.FC<FilterPanelProps> = ({
  filters,
  onCategoryChange,
  onToggleTier,
  onToggleTag,
  onToggleAllergen,
  onSetZeroFlagsOnly,
  onClearFilters,
  hideCategoryFilter = false,
  className,
}) => {
  const [openSections, setOpenSections] = useState<Record<string, boolean>>({
    category: true,
    tier: true,
    clean: true,
    tags: true,
    allergens: false,
  });

  const toggleSection = (section: string) => {
    setOpenSections((prev) => ({ ...prev, [section]: !prev[section] }));
  };

  const hasActiveFilters =
    (!hideCategoryFilter && Boolean(filters.categorySlug)) ||
    Boolean(filters.proteinTiers?.length) ||
    Boolean(filters.dietaryTags?.length) ||
    Boolean(filters.excludeAllergens?.length) ||
    Boolean(filters.zeroFlagsOnly);

  return (
    <div
      className={cn(
        "flex flex-col gap-5 p-5 rounded-2xl bg-[rgba(18,18,26,0.7)] backdrop-blur-xl border border-[rgba(255,255,255,0.08)]",
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between pb-3 border-b border-[rgba(255,255,255,0.06)]">
        <div className="flex items-center gap-2">
          <span className="text-sm font-bold text-[var(--text-primary)]">Faceted Filters</span>
          {hasActiveFilters && (
            <Badge variant="clean" size="sm">
              Active
            </Badge>
          )}
        </div>
        {hasActiveFilters && (
          <button
            type="button"
            onClick={onClearFilters}
            className="text-xs text-[var(--accent-emerald)] hover:underline cursor-pointer"
          >
            Clear All
          </button>
        )}
      </div>

      {/* Zero Red Flags Toggle */}
      <div className="flex items-center justify-between p-3 rounded-xl bg-[rgba(0,212,170,0.06)] border border-[rgba(0,212,170,0.2)]">
        <div className="flex flex-col">
          <span className="text-xs font-bold text-white flex items-center gap-1.5">
            <span>✨</span>
            <span>Zero Red Flags Only</span>
          </span>
          <span className="text-[11px] text-[var(--text-muted)]">
            Hide products with maltitol or spiking
          </span>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            className="sr-only peer"
            checked={Boolean(filters.zeroFlagsOnly)}
            onChange={(e) => onSetZeroFlagsOnly(e.target.checked)}
          />
          <div className="w-9 h-5 bg-[rgba(255,255,255,0.15)] peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-4 after:w-4 after:transition-all peer-checked:bg-[var(--accent-emerald)]" />
        </label>
      </div>

      {/* Category Section */}
      {!hideCategoryFilter && (
        <div className="flex flex-col gap-2.5">
          <button
            type="button"
            onClick={() => toggleSection("category")}
            className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)] hover:text-white"
          >
            <span>Category</span>
            <span>{openSections.category ? "−" : "+"}</span>
          </button>
          {openSections.category && (
            <div className="flex flex-col gap-1.5 pt-1">
              <button
                type="button"
                onClick={() => onCategoryChange?.(undefined)}
                className={cn(
                  "flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left",
                  !filters.categorySlug
                    ? "bg-[rgba(0,212,170,0.15)] text-[var(--accent-emerald)] font-semibold"
                    : "text-[var(--text-muted)] hover:bg-[rgba(255,255,255,0.05)] hover:text-white"
                )}
              >
                <span>All Categories</span>
              </button>
              {CATEGORIES.map((cat) => (
                <button
                  key={cat.slug}
                  type="button"
                  onClick={() => onCategoryChange?.(cat.slug)}
                  className={cn(
                    "flex items-center justify-between px-2.5 py-1.5 rounded-lg text-xs transition-colors text-left",
                    filters.categorySlug === cat.slug
                      ? "bg-[rgba(0,212,170,0.15)] text-[var(--accent-emerald)] font-semibold"
                      : "text-[var(--text-muted)] hover:bg-[rgba(255,255,255,0.05)] hover:text-white"
                  )}
                >
                  <span className="flex items-center gap-2">
                    <span>{cat.icon}</span>
                    <span>{cat.name}</span>
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Protein Tier Section */}
      <div className="flex flex-col gap-2.5 pt-2 border-t border-[rgba(255,255,255,0.06)]">
        <button
          type="button"
          onClick={() => toggleSection("tier")}
          className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)] hover:text-white"
        >
          <span>Protein Quality Tier</span>
          <span>{openSections.tier ? "−" : "+"}</span>
        </button>
        {openSections.tier && (
          <div className="flex flex-col gap-2 pt-1">
            {Object.entries(PROTEIN_TIERS).map(([tierKey, config]) => {
              const isChecked = filters.proteinTiers?.includes(tierKey) || false;
              return (
                <label
                  key={tierKey}
                  className="flex items-start gap-2.5 text-xs text-[var(--text-secondary)] cursor-pointer hover:text-white select-none"
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => onToggleTier(tierKey)}
                    className="mt-0.5 rounded border-[rgba(255,255,255,0.2)] bg-[rgba(255,255,255,0.05)] text-[var(--accent-emerald)] focus:ring-0"
                  />
                  <div className="flex flex-col">
                    <span className="font-semibold">{config.badgeLabel}</span>
                    <span className="text-[10px] text-[var(--text-faint)] leading-tight">
                      {tierKey === "Tier 1" && "Isolates (>90%)"}
                      {tierKey === "Tier 2" && "Concentrates (70-80%)"}
                      {tierKey === "Tier 3" && "Complete Plant Blends"}
                      {tierKey === "Tier 4" && "Incomplete / Collagen"}
                    </span>
                  </div>
                </label>
              );
            })}
          </div>
        )}
      </div>

      {/* Dietary Tags Section */}
      <div className="flex flex-col gap-2.5 pt-2 border-t border-[rgba(255,255,255,0.06)]">
        <button
          type="button"
          onClick={() => toggleSection("tags")}
          className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)] hover:text-white"
        >
          <span>Dietary Preferences</span>
          <span>{openSections.tags ? "−" : "+"}</span>
        </button>
        {openSections.tags && (
          <div className="flex flex-wrap gap-1.5 pt-1">
            {DIETARY_TAGS_LIST.map((tag) => {
              const isSelected =
                filters.dietaryTags?.some((t) => t.toLowerCase() === tag.value.toLowerCase()) ||
                false;
              return (
                <button
                  key={tag.value}
                  type="button"
                  onClick={() => onToggleTag(tag.value)}
                  className={cn(
                    "px-2.5 py-1 rounded-full text-xs font-medium border transition-colors select-none",
                    isSelected
                      ? "bg-[rgba(0,212,170,0.18)] text-[#00d4aa] border-[rgba(0,212,170,0.4)]"
                      : "bg-[rgba(255,255,255,0.04)] text-[var(--text-muted)] border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.2)] hover:text-white"
                  )}
                >
                  {tag.label}
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Allergen Exclusions */}
      <div className="flex flex-col gap-2.5 pt-2 border-t border-[rgba(255,255,255,0.06)]">
        <button
          type="button"
          onClick={() => toggleSection("allergens")}
          className="flex items-center justify-between text-xs font-bold uppercase tracking-wider text-[var(--text-secondary)] hover:text-white"
        >
          <span>Exclude Allergens</span>
          <span>{openSections.allergens ? "−" : "+"}</span>
        </button>
        {openSections.allergens && (
          <div className="flex flex-col gap-1.5 pt-1">
            <span className="text-[10px] text-[var(--text-faint)]">
              Products with these allergens will be hidden:
            </span>
            {ALLERGENS_LIST.map((allergen) => {
              const isExcluded =
                filters.excludeAllergens?.some(
                  (a) => a.toLowerCase() === allergen.value.toLowerCase()
                ) || false;
              return (
                <label
                  key={allergen.value}
                  className="flex items-center gap-2 text-xs text-[var(--text-secondary)] cursor-pointer hover:text-white select-none"
                >
                  <input
                    type="checkbox"
                    checked={isExcluded}
                    onChange={() => onToggleAllergen(allergen.value)}
                    className="rounded border-[rgba(255,255,255,0.2)] bg-[rgba(255,255,255,0.05)] text-[var(--accent-red)] focus:ring-0"
                  />
                  <span>Exclude {allergen.label}</span>
                </label>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
