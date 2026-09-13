"use client";

import React, { useState, useRef, useEffect } from "react";
import { SORT_OPTIONS } from "@/lib/constants";
import { cn } from "@/lib/utils";

export interface SortDropdownProps {
  currentSort?: string;
  onSortChange: (sortValue: string) => void;
}

export const SortDropdown: React.FC<SortDropdownProps> = ({
  currentSort = "cost_per_g_asc",
  onSortChange,
}) => {
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const selectedOption =
    SORT_OPTIONS.find((opt) => opt.value === currentSort) || SORT_OPTIONS[0];

  useEffect(() => {
    const handleClickOutside = (e: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(e.target as Node)) {
        setIsOpen(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  return (
    <div className="relative inline-block text-left" ref={dropdownRef}>
      <button
        type="button"
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3.5 py-2 text-xs font-semibold rounded-xl bg-[rgba(255,255,255,0.04)] border border-[rgba(255,255,255,0.08)] hover:border-[rgba(255,255,255,0.2)] text-[var(--text-primary)] transition-all select-none"
      >
        <span className="text-[var(--text-muted)]">Sort by:</span>
        <span className="text-[var(--accent-emerald)]">{selectedOption.label}</span>
        <svg
          className={cn("w-3.5 h-3.5 transition-transform", isOpen && "rotate-180")}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-1.5 w-64 rounded-xl bg-[#161622] border border-[rgba(255,255,255,0.12)] shadow-2xl backdrop-blur-2xl py-1 animate-fade-in overflow-hidden">
          {SORT_OPTIONS.map((opt) => {
            const isSelected = opt.value === currentSort;
            return (
              <button
                key={opt.value}
                type="button"
                onClick={() => {
                  onSortChange(opt.value);
                  setIsOpen(false);
                }}
                className={cn(
                  "w-full text-left px-3.5 py-2 text-xs transition-colors flex items-center justify-between",
                  isSelected
                    ? "bg-[rgba(0,212,170,0.12)] text-[var(--accent-emerald)] font-bold"
                    : "text-[var(--text-secondary)] hover:bg-[rgba(255,255,255,0.05)] hover:text-white"
                )}
              >
                <span>{opt.label}</span>
                {isSelected && <span>✓</span>}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};
