"use client";

import React from "react";
import { useCart } from "@/context/CartContext";
import { cn } from "@/lib/utils";

export interface CartButtonProps {
  className?: string;
  hideTextOnMobile?: boolean;
}

export const CartButton: React.FC<CartButtonProps> = ({
  className,
  hideTextOnMobile = false,
}) => {
  const { itemCount, openCart } = useCart();

  return (
    <button
      type="button"
      onClick={openCart}
      aria-label={`View Shortlist (${itemCount} items)`}
      className={cn(
        "group relative flex items-center gap-1.5 sm:gap-2 min-h-[36px] sm:min-h-[34px] rounded-xl text-xs sm:text-sm font-sans font-bold tracking-tight whitespace-nowrap cursor-pointer shrink-0 border select-none touch-manipulation",
        hideTextOnMobile ? "max-md:px-2.5 px-3 sm:px-4" : "px-2.5 sm:px-4",
        "bg-[#1C1916]/85 text-[#968E85] border-[#332D27]",
        "md:hover:bg-[#26221E] md:hover:text-[#F5F2EB] md:hover:border-[#D97706]/50 md:hover:shadow-[0_0_16px_rgba(217,119,6,0.18),0_2px_8px_rgba(0,0,0,0.4)]",
        "active:scale-[0.98]",
        "transition-all duration-300 ease-out",
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
        className="transition-colors duration-300 text-[#968E85] md:group-hover:text-[#D97706] shrink-0"
      >
        <circle cx="8" cy="21" r="1" />
        <circle cx="19" cy="21" r="1" />
        <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" />
      </svg>
      <span
        className={cn(
          "tracking-tight transition-colors duration-300 font-bold",
          hideTextOnMobile ? "max-md:hidden" : "inline"
        )}
      >
        Cart
      </span>

      {/* Item count badge */}
      {itemCount > 0 && (
        <span className="min-w-[18px] h-[18px] px-1 rounded-full bg-[#D97706] text-white text-[10px] font-black flex items-center justify-center font-mono shadow-[0_0_8px_rgba(217,119,6,0.4)] transition-all duration-300 md:group-hover:scale-105 md:group-hover:shadow-[0_0_12px_rgba(217,119,6,0.7)] ml-0.5">
          {itemCount}
        </span>
      )}
    </button>
  );
};
