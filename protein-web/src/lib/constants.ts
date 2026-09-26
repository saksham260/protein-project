export const CATEGORIES = [
  {
    name: "Protein Powders",
    slug: "protein-powders",
    description: "Whey isolates, concentrates, plant protein blends, and casein powders.",
    icon: "🥛",
  },
  {
    name: "Protein Bars",
    slug: "protein-bars",
    description: "On-the-go snack bars analyzed for hidden sugars, maltitol, and protein density.",
    icon: "🍫",
  },
  {
    name: "RTD Drinks",
    slug: "rtd-drinks",
    description: "Ready-to-drink high protein milkshakes, lassi, buttermilk, and greek yogurt.",
    icon: "🥤",
  },
  {
    name: "Savory Snacks",
    slug: "savory-snacks",
    description: "Protein chips, namkeen mixtures, crisps, and roasted savory protein bites.",
    icon: "🥨",
  },
] as const;

export const SORT_OPTIONS = [
  { label: "Cost per Gram (₹/g) — Low to High", value: "cost_per_g_asc", column: "best_cost_per_g_protein", ascending: true },
  { label: "Protein Density — High to Low", value: "density_desc", column: "protein_density_pct", ascending: false },
  { label: "Protein per ₹100 — High to Low", value: "p100_desc", column: "best_cost_per_g_protein", ascending: true },
  { label: "Calories per g Protein — Low to High", value: "kcal_per_g_asc", column: "calories_kcal", ascending: true },
  { label: "Best Price — Low to High", value: "best_price_asc", column: "best_price_inr", ascending: true },
  { label: "MRP — Low to High", value: "price_asc", column: "mrp_inr", ascending: true },
  { label: "MRP — High to Low", value: "price_desc", column: "mrp_inr", ascending: false },
  { label: "Protein per Serving — High to Low", value: "protein_desc", column: "protein_g", ascending: false },
] as const;

export const PROTEIN_TIERS = {
  "Tier 1": {
    label: "Tier 1: Pure Isolate / Hydrolysate",
    badgeLabel: "Tier 1: Pure Isolate",
    color: "#00d4aa",
    bg: "rgba(0, 212, 170, 0.15)",
    border: "rgba(0, 212, 170, 0.4)",
    description: "Highest bioavailability and purity (>90% protein, minimal lactose/fat). Whey protein isolate, native whey, micellar casein.",
  },
  "Tier 2": {
    label: "Tier 2: Concentrate / Blends",
    badgeLabel: "Tier 2: Concentrate",
    color: "#38bdf8",
    bg: "rgba(56, 189, 248, 0.15)",
    border: "rgba(56, 189, 248, 0.4)",
    description: "Solid bioavailability (70–80% protein). Whey protein concentrate, milk protein concentrate, isolate/concentrate blends.",
  },
  "Tier 3": {
    label: "Tier 3: Plant Protein Blends",
    badgeLabel: "Tier 3: Plant Blend",
    color: "#fbbf24",
    bg: "rgba(251, 191, 36, 0.15)",
    border: "rgba(251, 191, 36, 0.4)",
    description: "Complete amino acid profile achieved through pea + brown rice or multi-seed plant blends.",
  },
  "Tier 4": {
    label: "Tier 4: Incomplete / Spiked / Collagen",
    badgeLabel: "Tier 4: Incomplete / Spiked",
    color: "#f87171",
    bg: "rgba(248, 113, 113, 0.15)",
    border: "rgba(248, 113, 113, 0.4)",
    description: "Non-muscle building proteins (collagen, gelatin, wheat gluten) or products flagged for amino spiking.",
  },
} as const;

export const ALLERGENS_LIST = [
  { label: "Milk / Dairy", value: "milk" },
  { label: "Soy", value: "soy" },
  { label: "Gluten / Wheat", value: "gluten" },
  { label: "Tree Nuts", value: "tree_nuts" },
  { label: "Peanuts", value: "peanuts" },
  { label: "Eggs", value: "eggs" },
] as const;

export const DIETARY_TAGS_LIST = [
  { label: "Vegetarian", value: "vegetarian" },
  { label: "Vegan", value: "vegan" },
  { label: "Keto Friendly", value: "keto" },
  { label: "Gluten-Free", value: "gluten-free" },
  { label: "No Added Sugar", value: "no-added-sugar" },
  { label: "Clean Label", value: "clean-label" },
] as const;

export const PLATFORM_INFO = {
  amazon: { name: "Amazon", color: "#FF9900", icon: "📦" },
  blinkit: { name: "Blinkit", color: "#F8CB46", icon: "⚡" },
  zepto: { name: "Zepto", color: "#7B2CBF", icon: "🚀" },
  instamart: { name: "Instamart", color: "#FC8019", icon: "🛵" },
  d2c: { name: "Brand Store", color: "#00D4AA", icon: "🏪" },
} as const;
