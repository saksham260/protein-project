import React from "react";
import { Badge } from "@/components/ui/Badge";
import { Tooltip } from "@/components/ui/Tooltip";
import { VariantRedFlag } from "@/types/product";

export interface RedFlagBadgesProps {
  flags: VariantRedFlag[] | undefined | null;
  compact?: boolean;
}

export const RedFlagBadges: React.FC<RedFlagBadgesProps> = ({ flags = [], compact = false }) => {
  const flagList = flags || [];

  if (flagList.length === 0) {
    return (
      <Badge variant="clean" size={compact ? "sm" : "md"} dot>
        Zero Red Flags
      </Badge>
    );
  }

  if (compact) {
    const highSeverityCount = flagList.filter((f) => f.flag_severity === "high").length;
    const badgeVariant = highSeverityCount > 0 ? "danger" : "warning";

    const tooltipContent = (
      <div className="flex flex-col gap-1.5">
        <p className="font-semibold text-[var(--text-primary)]">
          {flagList.length} Flag{flagList.length > 1 ? "s" : ""} Detected:
        </p>
        <ul className="list-disc pl-4 space-y-1 text-[var(--text-secondary)]">
          {flagList.map((flag) => (
            <li key={flag.id || flag.flag_label}>
              <strong className="text-[var(--text-primary)]">{flag.flag_label}</strong>
              {flag.matched_ingredient && ` (${flag.matched_ingredient})`}
            </li>
          ))}
        </ul>
      </div>
    );

    return (
      <Tooltip content={tooltipContent}>
        <Badge variant={badgeVariant} size="sm" dot>
          {flagList.length} Flag{flagList.length > 1 ? "s" : ""}
        </Badge>
      </Tooltip>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-1.5">
      {flagList.map((flag) => {
        const variant =
          flag.flag_severity === "high"
            ? "danger"
            : flag.flag_severity === "amber"
            ? "warning"
            : "info";

        return (
          <Tooltip
            key={flag.id || flag.flag_label}
            content={
              <div className="flex flex-col gap-1">
                <span className="font-bold">{flag.flag_label}</span>
                <p className="text-[var(--text-secondary)]">{flag.flag_description}</p>
                {flag.matched_ingredient && (
                  <span className="text-[var(--text-faint)] font-mono text-[10px]">
                    Matched: {flag.matched_ingredient}
                  </span>
                )}
              </div>
            }
          >
            <Badge variant={variant} size="sm" dot>
              {flag.flag_label}
            </Badge>
          </Tooltip>
        );
      })}
    </div>
  );
};
