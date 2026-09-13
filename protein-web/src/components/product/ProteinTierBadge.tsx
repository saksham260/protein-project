import React from "react";
import { Badge } from "@/components/ui/Badge";
import { Tooltip } from "@/components/ui/Tooltip";
import { PROTEIN_TIERS } from "@/lib/constants";
import { ProteinTier } from "@/types/product";

export interface ProteinTierBadgeProps {
  tier: ProteinTier | string | null | undefined;
  showTooltip?: boolean;
  size?: "sm" | "md";
}

export const ProteinTierBadge: React.FC<ProteinTierBadgeProps> = ({
  tier,
  showTooltip = true,
  size = "sm",
}) => {
  if (!tier) {
    return <Badge size={size} variant="default">Unrated Tier</Badge>;
  }

  const tierKey = (tier.startsWith("Tier") ? tier : `Tier ${tier}`) as keyof typeof PROTEIN_TIERS;
  const config = PROTEIN_TIERS[tierKey];

  const variantMap: Record<string, "tier1" | "tier2" | "tier3" | "tier4"> = {
    "Tier 1": "tier1",
    "Tier 2": "tier2",
    "Tier 3": "tier3",
    "Tier 4": "tier4",
  };

  const badgeVariant = variantMap[tierKey] || "default";
  const label = config ? config.badgeLabel : tier;

  const badgeElement = (
    <Badge size={size} variant={badgeVariant} dot>
      {label}
    </Badge>
  );

  if (showTooltip && config) {
    return (
      <Tooltip content={<p className="leading-snug">{config.description}</p>}>
        {badgeElement}
      </Tooltip>
    );
  }

  return badgeElement;
};
