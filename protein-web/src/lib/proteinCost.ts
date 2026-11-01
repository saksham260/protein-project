import type { ProductVariant, ProductWithVariants } from "@/types/product";
import { bestValueVariant } from "@/lib/bestLists";
import { effectiveCostPerGram, proteinInPack } from "@/lib/metrics";

/** ICMR-NIN 2020: safe protein requirement for healthy Indian adults, in g per kg of body weight per day. */
export const ICMR_RDA_G_PER_KG = 0.83;

const DAYS_PER_MONTH = 30;
const RESULTS_SHOWN = 10;

export function icmrReferenceGrams(weightKg: number): number {
  return Math.round(weightKg * ICMR_RDA_G_PER_KG);
}

export interface CostOptions {
  gramsPerDay: number;
  categorySlug?: string;
  diet?: "vegetarian" | "vegan";
  hideRedFlags?: boolean;
}

export interface CostResult {
  product: ProductWithVariants;
  variant: ProductVariant;
  perDay: number;
  perMonth: number;
  packsPerMonth: number;
}

function costOf(product: ProductWithVariants, variant: ProductVariant, gramsPerDay: number): CostResult | null {
  const costPerGram = effectiveCostPerGram(variant);
  const packProtein = proteinInPack(variant);
  if (costPerGram === null || packProtein <= 0) return null;
  const perDay = costPerGram * gramsPerDay;
  return {
    product,
    variant,
    perDay,
    perMonth: perDay * DAYS_PER_MONTH,
    packsPerMonth: (gramsPerDay * DAYS_PER_MONTH) / packProtein,
  };
}

/** What each product would cost for this much protein a day, cheapest first. */
export function rankByDailyCost(products: ProductWithVariants[], options: CostOptions): CostResult[] {
  const { gramsPerDay, categorySlug, diet, hideRedFlags } = options;
  const results: CostResult[] = [];

  for (const product of products) {
    if (categorySlug && product.category?.slug !== categorySlug) continue;
    const variant = bestValueVariant(product, (v) => {
      if (diet && !v.dietary_tags.includes(diet)) return false;
      return !hideRedFlags || (v.ingredient_list.length > 0 && (v.red_flags ?? []).length === 0);
    });
    const result = variant && costOf(product, variant, gramsPerDay);
    if (result) results.push(result);
  }

  return results.sort((a, b) => a.perDay - b.perDay).slice(0, RESULTS_SHOWN);
}
