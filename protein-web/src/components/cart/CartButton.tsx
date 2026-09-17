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
        "relative flex items-center justify-center p-2 rounded-full bg-[#18181B] hover:bg-[#27272A] border border-[#27272A] hover:border-[#3F3F46] text-[#E4E4E7] hover:text-white transition-all shadow-sm active:scale-95 cursor-pointer",
        className
      )}
    >
      <svg
        width="18"
        height="18"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      >
        <circle cx="8" cy="21" r="1" />
        <circle cx="19" cy="21" r="1" />
        <path d="M2.05 2.05h2l2.66 12.42a2 2 0 0 0 2 1.58h9.78a2 2 0 0 0 1.95-1.57l1.65-7.43H5.12" />
      </svg>

      {/* Item count badge */}
      {itemCount > 0 && (
        <span className="absolute -top-1 -right-1 min-w-[18px] h-[18px] px-1 rounded-full bg-[#10B981] text-[#0A0A0B] text-[10px] font-black flex items-center justify-center font-mono shadow-[0_0_10px_rgba(16,185,129,0.5)] animate-in zoom-in-50 duration-150">
          {itemCount}
        </span>
      )}
    </button>
  );
};
