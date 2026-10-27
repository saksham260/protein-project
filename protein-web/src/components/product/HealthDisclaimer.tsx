"use client";

import React from "react";

export interface HealthDisclaimerProps {
  className?: string;
}

export const HealthDisclaimer: React.FC<HealthDisclaimerProps> = ({ className = "" }) => {
  return (
    <div
      role="note"
      aria-label="Health and dietary guidance notice"
      className={`relative overflow-hidden rounded-2xl p-4 sm:p-5 border border-amber-500/30 bg-gradient-to-r from-amber-500/10 via-[#18181B] to-amber-500/5 shadow-[0_8px_30px_rgba(245,158,11,0.08)] ${className}`}
    >
      <div className="flex items-start gap-3.5">
        <div className="shrink-0 w-8 h-8 rounded-xl bg-amber-500/20 border border-amber-500/40 flex items-center justify-center text-amber-400 mt-0.5">
          <svg
            className="w-4 h-4 stroke-[2.2]"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              d="M12 9v3.75m0-10.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.75c0 5.592 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.57-.598-3.75h-.002A11.959 11.959 0 0112 2.714zm0 14.036h.008v.008H12v-.008z"
            />
          </svg>
        </div>
        <div className="flex flex-col gap-1 text-left">
          <span className="text-xs font-mono uppercase tracking-wider text-amber-400 font-bold">
            Health &amp; Dietary Guidance Notice
          </span>
          <p className="text-xs sm:text-sm text-zinc-300 leading-relaxed font-sans">
            This product is a nutritional supplement, not a medicine. Consult your doctor or dietitian
            before use, especially if you are diabetic, pregnant, elderly, or buying for a child.
          </p>
        </div>
      </div>
    </div>
  );
};
