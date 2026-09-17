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
  displayMonth: string;
  displayYear: number;
  awards: AwardCategory[];
}

export const TOP_PICKS_CONFIG: TopPicksConfig = {
  displayMonth: "September",
  displayYear: 2026,
  awards: [
    {
      id: "best-protein-powder",
      label: "Best Protein Powder",
      description: "Top economic value and purity in verified protein powders.",
      glowColor: "#FFD700", // Gold
      badgeEmoji: "🥛",
      autoRule: {
        categorySlug: "protein-powders",
        sortBy: "cost_per_g_asc",
      },
    },
    {
      id: "best-protein-bar",
      label: "Best Protein Bar",
      description: "Top economic value in portable snack bars with zero compromise.",
      glowColor: "#CD7F32", // Bronze / Copper
      badgeEmoji: "🍫",
      autoRule: {
        categorySlug: "protein-bars",
        sortBy: "cost_per_g_asc",
      },
    },
    {
      id: "best-rtd-drink",
      label: "Best Ready-to-Drink",
      description: "Highest protein yield per rupee in ready-to-drink beverages.",
      glowColor: "#22D3EE", // Cyan
      badgeEmoji: "🥤",
      autoRule: {
        categorySlug: "rtd-drinks",
        sortBy: "cost_per_g_asc",
      },
    },
    {
      id: "best-snack",
      label: "Best Savory Snack",
      description: "Crispy high-protein crunch with lowest cost per gram of protein.",
      glowColor: "#F59E0B", // Amber
      badgeEmoji: "🥨",
      autoRule: {
        categorySlug: "savory-snacks",
        sortBy: "cost_per_g_asc",
      },
    },
  ],
};
