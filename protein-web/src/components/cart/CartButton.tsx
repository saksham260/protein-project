"use client";

import React from "react";
import { useCart } from "@/context/CartContext";
import { cn } from "@/lib/utils";

export interface CartButtonProps {
  className?: string;
}

export const CartButton: React.FC<CartButtonProps> = ({ className }) => {
  const { itemCount, openCart } = useCart();

  return (
    <button
      type="button"
      onClick={openCart}
      aria-label={`View Shortlist (${itemCount} items)`}
      className={cn(
        "group relative flex items-center gap-1.5 sm:gap-2 px-3 sm:px-4 py-1.5 min-h-[36px] sm:min-h-[34px] rounded-xl text-xs sm:text-sm font-sans font-bold tracking-tight whitespace-nowrap transition-all duration-200 cursor-pointer shrink-0 border active:scale-95 touch-manipulation select-none bg-[#1C1916]/85 text-[#968E85] border-[#332D27] hover:bg-[#D97706] hover:border-[#D97706] hover:!text-white",
        className
      )}
    >
      <svg
        width="16"
        height="16"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2.2"
        strokeLinecap="round"
        strokeLinejoin="round"
        className="transition-colors text-inherit group-hover:!text-white shrink-0"
      >
        <circle cx="8" cy="21" r="1" />
        <circle cx="19" cy="21" r="1" />
        <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" />
      </svg>
      <span className="tracking-tight text-inherit group-hover:!text-white font-bold">Cart</span>

      {/* Item count badge */}
      {itemCount > 0 && (
        <span className="min-w-[18px] h-[18px] px-1 rounded-full bg-[#D97706] group-hover:!bg-white text-white group-hover:!text-black text-[10px] font-black flex items-center justify-center font-mono shadow-sm transition-colors ml-0.5">
          {itemCount}
        </span>
      )}
    </button>
  );
};
