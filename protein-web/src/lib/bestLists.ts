import type { ProductVariant, ProductWithVariants } from "@/types/product";
import { computePer100g } from "@/lib/utils";
import { effectiveCostPerGram } from "@/lib/metrics";

const LIST_LENGTH = 10;

export interface BestList {
  slug: string;
  /** Short name for links. */
  name: string;
  title: string;
  description: string;
  /** Plain statement of what qualifies, shown on the page. */
  rule: string;
  categorySlug: string;
  matches: (v: ProductVariant) => boolean;
}

const hasTag = (v: ProductVariant, tag: string) => v.dietary_tags.includes(tag);
const ingredients = (v: ProductVariant) => v.ingredient_list.join(" ").toLowerCase();
const sugarsPer100g = (v: ProductVariant) => computePer100g(v.total_sugars_g, v.serving_size_g);

// Kept short on purpose: a few honest lists, not one page per search term.
export const BEST_LISTS: BestList[] = [
  {
    slug: "whey-isolate",
    name: "Whey Isolate",
    title: "Lowest Cost Whey Isolate in India",
    description: "Whey isolate powders in India ranked by cost per gram of protein, using label data and known store prices.",
    rule: "Protein powders whose main protein is whey isolate, with no whey concentrate on the ingredient list.",
    categorySlug: "protein-powders",
    // The source field names a blend's first protein, so blends need ruling out here.
    matches: (v) =>
      v.primary_protein_source === "Whey Protein Isolate" &&
      v.protein_tier === "Tier 1" &&
      !ingredients(v).includes("concentrate"),
  },
  {
    slug: "whey-concentrate",
    name: "Whey Concentrate",
    title: "Lowest Cost Whey Concentrate in India",
    description: "Whey concentrate powders in India ranked by cost per gram of protein, using label data and known store prices.",
    rule: "Protein powders whose main protein is whey concentrate.",
    categorySlug: "protein-powders",
    matches: (v) => v.primary_protein_source === "Whey Protein Concentrate",
  },
  {
    slug: "vegan-protein-powder",
    name: "Vegan Protein Powder",
    title: "Lowest Cost Vegan Protein Powders in India",
    description: "Vegan protein powders in India ranked by cost per gram of protein, using label data and known store prices.",
    rule: "Protein powders labelled vegan.",
    categorySlug: "protein-powders",
    matches: (v) => hasTag(v, "vegan"),
  },
  {
    slug: "protein-bars-without-maltitol",
    name: "Protein Bars Without Maltitol",
    title: "Lowest Cost Protein Bars Without Maltitol",
    description: "Protein bars in India with no maltitol on the ingredient list, ranked by cost per gram of protein.",
    rule: "Protein bars with no maltitol on the ingredient list.",
    categorySlug: "protein-bars",
    matches: (v) => !/maltitol|ins 965/.test(ingredients(v)),
  },
  {
    slug: "protein-bars-under-5g-sugar",
    name: "Protein Bars Under 5g Sugar",
    title: "Lowest Cost Protein Bars With Under 5g Sugar per 100g",
    description: "Protein bars in India with under 5g of sugars per 100g on the label, ranked by cost per gram of protein.",
    rule: "Protein bars with under 5g of total sugars per 100g on the label.",
    categorySlug: "protein-bars",
    matches: (v) => sugarsPer100g(v) < 5,
  },
  {
    slug: "peanut-butter-no-added-sugar",
    name: "Peanut Butter, No Added Sugar",
    title: "Lowest Cost Peanut Butter With No Added Sugar",
    description: "Peanut butters and spreads in India with no added sugar on the label, ranked by cost per gram of protein.",
    rule: "Peanut butters and spreads labelled no added sugar, with no sugar on the ingredient list.",
    categorySlug: "protein-spreads",
    matches: (v) => hasTag(v, "no-added-sugar"),
  },
];

/** The cheapest pack per gram of protein among a product's in-stock variants that pass `matches`. */
export function bestValueVariant(
  product: ProductWithVariants,
  matches: (v: ProductVariant) => boolean
): ProductVariant | null {
  let best: { variant: ProductVariant; cost: number } | null = null;
  for (const variant of product.variants) {
    const cost = effectiveCostPerGram(variant);
    if (cost === null || variant.is_available === false || !matches(variant)) continue;
    if (!best || cost < best.cost) best = { variant, cost };
  }
  return best?.variant ?? null;
}

/** Only products we could scan and found nothing on count, so a list never rewards missing data. */
function isCleanOnLabel(v: ProductVariant): boolean {
  return v.ingredient_list.length > 0 && (v.red_flags ?? []).length === 0;
}

export function buildBestList(products: ProductWithVariants[], list: BestList): ProductWithVariants[] {
  const ranked: { product: ProductWithVariants; cost: number }[] = [];
  for (const product of products) {
    if (product.category?.slug !== list.categorySlug) continue;
    const variant = bestValueVariant(product, (v) => isCleanOnLabel(v) && list.matches(v));
    const cost = variant ? effectiveCostPerGram(variant) : null;
    if (variant && cost !== null) {
      ranked.push({ product: { ...product, matched_variant_id: variant.id }, cost });
    }
  }
  return ranked
    .sort((a, b) => a.cost - b.cost)
    .slice(0, LIST_LENGTH)
    .map((entry) => entry.product);
}
