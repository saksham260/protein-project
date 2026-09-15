"use client";

import React, { useState } from "react";
import { CATEGORIES, PROTEIN_TIERS, ALLERGENS_LIST, DIETARY_TAGS_LIST } from "@/lib/constants";
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
        "flex flex-col gap-6 p-6 rounded-3xl bg-[#18181B] border border-[#27272A] shadow-[0_12px_40px_rgba(0,0,0,0.6)] select-none",
        className
      )}
    >
      {/* Header */}
      <div className="flex items-center justify-between pb-4 border-b border-[#27272A]">
        <div className="flex items-center gap-2">
          <span className="text-sm font-mono uppercase tracking-widest text-[#A1A1AA] font-semibold">
            Filters
          </span>
          {hasActiveFilters && (
            <span className="text-[10px] font-mono font-bold px-2 py-0.5 rounded-full bg-[#10B981] text-black">
              Active
            </span>
          )}
        </div>
        {hasActiveFilters && (
          <button
            type="button"
            onClick={onClearFilters}
            className="text-xs font-mono text-[#A1A1AA] hover:text-[#10B981] transition-colors cursor-pointer"
          >
            Reset
          </button>
        )}
      </div>

      {/* Zero Red Flags Only Toggle */}
      <div className="flex items-center justify-between p-4 rounded-2xl bg-[#27272A]/60 border border-[#27272A]">
        <div className="flex flex-col">
          <span className="text-xs font-bold text-white font-mono tracking-tight">
            Zero Red Flags Only
          </span>
          <span className="text-[11px] text-[#A1A1AA] mt-0.5">
            Hide maltitol, spiking, palm oil
          </span>
        </div>
        <label className="relative inline-flex items-center cursor-pointer">
          <input
            type="checkbox"
            className="sr-only peer"
            checked={Boolean(filters.zeroFlagsOnly)}
            onChange={(e) => onSetZeroFlagsOnly(e.target.checked)}
            aria-label="Toggle Zero Red Flags Only"
          />
          <div className="w-11 h-6 bg-zinc-800 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-black after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-[#10B981] peer-checked:after:bg-black" />
        </label>
      </div>

      {/* Category Section */}
      {!hideCategoryFilter && (
        <div className="flex flex-col gap-3">
          <button
            type="button"
            onClick={() => toggleSection("category")}
            className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-[#A1A1AA] hover:text-white transition-colors"
          >
            <span>Category</span>
            <span className="text-zinc-600 font-mono">{openSections.category ? "−" : "+"}</span>
          </button>

          {openSections.category && (
            <div className="flex flex-col gap-1 pt-1">
              <button
                type="button"
                onClick={() => onCategoryChange?.(undefined)}
                className={cn(
                  "flex items-center justify-between px-3 py-2 rounded-xl text-xs font-mono transition-colors text-left",
                  !filters.categorySlug
                    ? "bg-[#10B981]/15 text-[#34D399] font-bold"
                    : "text-[#A1A1AA] hover:bg-[#27272A] hover:text-white"
                )}
              >
                <span>All Categories</span>
              </button>

              {CATEGORIES.map((cat) => {
                const isSelected = filters.categorySlug === cat.slug;
                return (
                  <button
                    key={cat.slug}
                    type="button"
                    onClick={() => onCategoryChange?.(cat.slug)}
                    className={cn(
                      "flex items-center justify-between px-3 py-2 rounded-xl text-xs font-mono transition-colors text-left",
                      isSelected
                        ? "bg-[#10B981]/15 text-[#34D399] font-bold"
                        : "text-[#A1A1AA] hover:bg-[#27272A] hover:text-white"
                    )}
                  >
                    <span>{cat.name}</span>
                    {isSelected && <span className="text-[#10B981] text-xs">●</span>}
                  </button>
                );
              })}
            </div>
          )}
        </div>
      )}

      {/* Protein Quality Tier Section */}
      <div className="flex flex-col gap-3 pt-3 border-t border-[#27272A]">
        <button
          type="button"
          onClick={() => toggleSection("tier")}
          className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-[#A1A1AA] hover:text-white transition-colors"
        >
          <span>Protein Quality Tier</span>
          <span className="text-zinc-600 font-mono">{openSections.tier ? "−" : "+"}</span>
        </button>

        {openSections.tier && (
          <div className="flex flex-col gap-2.5 pt-1">
            {Object.entries(PROTEIN_TIERS).map(([tierKey, config]) => {
              const isChecked = filters.proteinTiers?.includes(tierKey) || false;
              const isTier1 = tierKey === "Tier 1";

              return (
                <label
                  key={tierKey}
                  className="flex items-start gap-3 text-xs cursor-pointer group select-none"
                >
                  <input
                    type="checkbox"
                    checked={isChecked}
                    onChange={() => onToggleTier(tierKey)}
                    className="mt-0.5 rounded border-[#3F3F46] bg-[#27272A] text-[#10B981] focus:ring-0 focus:ring-offset-0 cursor-pointer accent-[#10B981]"
                  />
                  <div className="flex flex-col">
                    <span className={cn("font-mono font-medium transition-colors", isChecked ? "text-white font-bold" : "text-[#E4E4E7] group-hover:text-white")}>
                      {config.badgeLabel}
                      {isTier1 && <span className="text-[#34D399] ml-1.5 text-[10px] font-bold">★ ELITE</span>}
                    </span>
                    <span className="text-[10px] font-mono text-[#A1A1AA] leading-tight">
                      {tierKey === "Tier 1" && "Isolates (>90% pure)"}
                      {tierKey === "Tier 2" && "Concentrates (70-80%)"}
                      {tierKey === "Tier 3" && "Complete Plant Blends"}
                      {tierKey === "Tier 4" && "Incomplete / Fillers"}
                    </span>
                  </div>
                </label>
              );
            })}
          </div>
        )}
      </div>

      {/* Dietary Preferences Section */}
      <div className="flex flex-col gap-3 pt-3 border-t border-[#27272A]">
        <button
          type="button"
          onClick={() => toggleSection("tags")}
          className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-[#A1A1AA] hover:text-white transition-colors"
        >
          <span>Dietary Profile</span>
          <span className="text-zinc-600 font-mono">{openSections.tags ? "−" : "+"}</span>
        </button>

        {openSections.tags && (
          <div className="flex flex-wrap gap-2 pt-1">
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
                    "px-3 py-1.5 rounded-full text-xs font-mono transition-all duration-200 cursor-pointer",
                    isSelected
                      ? "bg-[#10B981] text-black font-bold shadow-[0_0_12px_rgba(16,185,129,0.25)]"
                      : "bg-[#27272A] text-[#A1A1AA] border border-[#3F3F46] hover:border-[#52525B] hover:text-white"
                  )}
                >
                  {tag.label}
                </button>
              );
            })}
          </div>
        )}
      </div>

      {/* Allergen Exclusions Section */}
      <div className="flex flex-col gap-3 pt-3 border-t border-[#27272A]">
        <button
          type="button"
          onClick={() => toggleSection("allergens")}
          className="flex items-center justify-between text-xs font-mono uppercase tracking-wider text-[#A1A1AA] hover:text-white transition-colors"
        >
          <span>Exclude Allergens</span>
          <span className="text-zinc-600 font-mono">{openSections.allergens ? "−" : "+"}</span>
        </button>

        {openSections.allergens && (
          <div className="flex flex-col gap-2 pt-1">
            <span className="text-[10px] font-mono text-[#A1A1AA]">
              Hide products containing:
            </span>
            {ALLERGENS_LIST.map((allergen) => {
              const isExcluded =
                filters.excludeAllergens?.some(
                  (a) => a.toLowerCase() === allergen.value.toLowerCase()
                ) || false;
              return (
                <label
                  key={allergen.value}
                  className="flex items-center gap-2.5 text-xs font-mono text-[#A1A1AA] hover:text-white cursor-pointer select-none"
                >
                  <input
                    type="checkbox"
                    checked={isExcluded}
                    onChange={() => onToggleAllergen(allergen.value)}
                    className="rounded border-[#3F3F46] bg-[#27272A] text-[#EF4444] focus:ring-0 accent-[#EF4444]"
                  />
                  <span className={isExcluded ? "text-[#F87171] font-bold" : ""}>
                    Exclude {allergen.label}
                  </span>
                </label>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};
