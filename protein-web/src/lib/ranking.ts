/**
 * Default ("Featured") display order for product lists:
 *   1. Individual items first, multi-packs next, combos / bundles last.
 *   2. Within each of those, bigger, better-known brands first.
 *   3. Then the lowest cost per gram of protein.
 * Picking any other sort option (e.g. cheapest protein) ignores all of this.
 */

/** 0 = individual item, 1 = multi-pack of the same item, 2 = combo / bundle / free gift. */
export type BundleLevel = 0 | 1 | 2;

const COMBO_PATTERN = /\b(combo|bundle|variety|assorted|sampler|hamper|starter kit|trial pack)\b|\+\s*free\b/i;
const MULTI_PACK_PATTERN = /\b(?:pack|box|case|carton|set)\s+of\s+(?:[2-9]|\d{2,})\b(?!\s+sachets?\b)|\b(?:[2-9]|\d{2,})\s*[- ]?packs?\b|\bmulti-?pack\b/i;

export function bundleLevel(productName: string, variantName: string, isCombo?: boolean): BundleLevel {
  const text = `${productName} ${variantName}`;
  if (isCombo || COMBO_PATTERN.test(text)) return 2;
  if (MULTI_PACK_PATTERN.test(text)) return 1;
  return 0;
}

/**
 * How well known a brand is in India: 1 = household names, 2 = well known, 3 = everyone else.
 * Edit these lists to change the order; names are matched ignoring upper/lower case.
 */
const BRAND_TIERS: Record<1 | 2, string[]> = {
  1: [
    "MuscleBlaze",
    "Optimum Nutrition",
    "Isopure",
    "GNC India",
    "Amul",
    "Yoga Bar",
    "The Whole Truth",
    "Fast&Up",
    "Max Protein",
    "RiteBite Max Protein",
    "MyFitness",
    "Pintola",
    "Epigamia",
    "Bagrry's",
  ],
  2: [
    "Avvatar",
    "Beastlife",
    "Wellbeing Nutrition",
    "Muscle Nectar",
    "Nutrabay",
    "Chase",
    "SuperYou",
    "Alpino",
    "Open Secret",
    "True Elements",
    "Sleepy Owl",
    "Plix",
    "Kapiva",
    "Nakpro",
    "Phab",
    "Naturaltein",
    "One Science Nutrition",
    "AS-IT-IS Nutrition",
    "Bolt Nutrition",
    "Scitron",
    "Eat Anytime",
    "Bigmuscles Nutrition",
    "XLR8 Sports Nutrition",
    "Origin Nutrition",
  ],
};

const TIER_BY_BRAND = new Map<string, 1 | 2>(
  ([1, 2] as const).flatMap((tier) => BRAND_TIERS[tier].map((name) => [name.toLowerCase(), tier] as [string, 1 | 2]))
);

export function brandTier(brandName: string | undefined): 1 | 2 | 3 {
  return TIER_BY_BRAND.get((brandName ?? "").trim().toLowerCase()) ?? 3;
}

/** Lower sorts first. Bundle level outranks brand tier, which outranks cost per gram (kept under 1000). */
export function featuredScore(args: {
  productName: string;
  variantName: string;
  isCombo?: boolean;
  brandName?: string;
  costPerGram: number | null;
}): number {
  const cost = Math.min(args.costPerGram ?? 999, 999);
  return (
    bundleLevel(args.productName, args.variantName, args.isCombo) * 10_000 +
    brandTier(args.brandName) * 1_000 +
    cost
  );
}
