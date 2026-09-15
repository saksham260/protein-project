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
        className="flex items-center gap-2 px-4 py-2 text-xs font-mono rounded-full bg-[#18181B] border border-[#27272A] hover:border-[#3F3F46] text-white transition-all select-none shadow-[0_4px_16px_rgba(0,0,0,0.4)]"
      >
        <span className="text-[#A1A1AA] uppercase tracking-wider text-[10px]">Sort:</span>
        <span className="font-semibold text-white">{selectedOption.label}</span>
        <svg
          className={cn("w-3 h-3 text-[#A1A1AA] transition-transform duration-200", isOpen && "rotate-180")}
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
        </svg>
      </button>

      {isOpen && (
        <div className="absolute right-0 z-50 mt-2 w-64 rounded-2xl bg-[#18181B] border border-[#27272A] shadow-[0_20px_50px_rgba(0,0,0,0.9)] py-1.5 animate-fade-in overflow-hidden">
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
                  "w-full text-left px-4 py-2.5 text-xs transition-colors flex items-center justify-between font-mono",
                  isSelected
                    ? "bg-[#10B981]/15 text-[#34D399] font-bold"
                    : "text-[#E4E4E7] hover:bg-[#27272A] hover:text-white"
                )}
              >
                <span>{opt.label}</span>
                {isSelected && <span className="text-[#10B981]">✓</span>}
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
};
