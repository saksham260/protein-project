import React from "react";

export interface AwardBadgeProps {
  label: string;
  emoji: string;
  glowColor: string;
}

export const AwardBadge: React.FC<AwardBadgeProps> = ({
  label,
  emoji,
  glowColor,
}) => {
  return (
    <div
      className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-bold tracking-tight shadow-lg backdrop-blur-md border select-none whitespace-nowrap transition-transform duration-300 group-hover:scale-105"
      style={{
        backgroundColor: "rgba(24, 24, 27, 0.94)",
        borderColor: glowColor,
        color: "#FFFFFF",
        boxShadow: `0 4px 16px ${glowColor}33`,
      }}
    >
      <span className="text-sm leading-none">{emoji}</span>
      <span
        className="font-mono text-[11px] font-black uppercase tracking-wider"
        style={{ color: glowColor }}
      >
        {label}
      </span>
    </div>
  );
};
