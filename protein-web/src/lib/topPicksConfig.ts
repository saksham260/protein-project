export interface AutoRule {
  categorySlug?: string;
  sortBy?: string;
  requireZeroFlags?: boolean;
  requireTier?: string;
}

export interface ManualOverride {
  productSlug: string;
  editorialBlurb?: string;
}

export interface AwardCategory {
  id: string;
  label: string;
  description: string;
  glowColor: string;
  badgeEmoji: string;
  autoRule: AutoRule;
  manualOverride?: ManualOverride;
}

export interface TopPicksConfig {
  awards: AwardCategory[];
}

// Picked by formula: the lowest cost per gram among in-stock products with no label red flags.
export const TOP_PICKS_CONFIG: TopPicksConfig = {
  awards: [
    {
      id: "best-protein-powder",
      label: "Best Value Protein Powder",
      description: "Lowest cost per gram among protein powders with no label red flags.",
      glowColor: "#FFD700", // Gold
      badgeEmoji: "🥛",
      autoRule: {
        categorySlug: "protein-powders",
        sortBy: "cost_per_g_asc",
        requireZeroFlags: true,
      },
    },
    {
      id: "best-protein-bar",
      label: "Best Value Protein Bar",
      description: "Lowest cost per gram among protein bars with no label red flags.",
      glowColor: "#CD7F32", // Bronze / Copper
      badgeEmoji: "🍫",
      autoRule: {
        categorySlug: "protein-bars",
        sortBy: "cost_per_g_asc",
        requireZeroFlags: true,
      },
    },
    {
      id: "best-rtd-drink",
      label: "Best Value Ready-to-Drink",
      description: "Lowest cost per gram among ready-to-drink products with no label red flags.",
      glowColor: "#22D3EE", // Cyan
      badgeEmoji: "🥤",
      autoRule: {
        categorySlug: "rtd-drinks",
        sortBy: "cost_per_g_asc",
        requireZeroFlags: true,
      },
    },
    {
      id: "best-snack",
      label: "Best Value Savory Snack",
      description: "Lowest cost per gram among savory snacks with no label red flags.",
      glowColor: "#F59E0B", // Amber
      badgeEmoji: "🥨",
      autoRule: {
        categorySlug: "savory-snacks",
        sortBy: "cost_per_g_asc",
        requireZeroFlags: true,
      },
    },
    {
      id: "best-spread",
      label: "Best Value Peanut Butter",
      description: "Lowest cost per gram among peanut butters and spreads with no label red flags.",
      glowColor: "#A16207", // Peanut brown
      badgeEmoji: "🥜",
      autoRule: {
        categorySlug: "protein-spreads",
        sortBy: "cost_per_g_asc",
        requireZeroFlags: true,
      },
    },
  ],
};
