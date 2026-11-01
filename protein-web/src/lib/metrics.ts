import { ProductVariant } from "@/types/product";

// Derived protein metrics. Formulas are documented in documentation/phase3-pricing-metrics-location-plan.md.

/** ₹ per gram of protein at the best known price, falling back to MRP. Lower is better. */
export function effectiveCostPerGram(v: ProductVariant): number | null {
  return v.best_cost_per_g_protein ?? v.cost_per_g_protein ?? null;
}

/** What the shopper is likely to pay: the lowest known store price, or MRP when none is known. */
export function sellingPrice(v: ProductVariant): number {
  return v.best_price_inr ?? v.mrp_inr;
}

/** Label for sellingPrice(): a store price that isn't below MRP mustn't be presented as the MRP. */
export function priceLabel(v: ProductVariant): "From" | "Price" | "MRP" {
  if (v.best_price_inr == null) return "MRP";
  return v.best_price_inr < v.mrp_inr ? "From" : "Price";
}

/** Total protein in the pack. Labels give it per serving; single-serve items have serving = pack. */
export function proteinInPack(v: ProductVariant): number {
  return v.serving_size_g > 0 ? (v.protein_g * v.net_weight_g) / v.serving_size_g : v.protein_g;
}

/** ₹ per gram of the protein a lab actually measured, rather than the amount on the label. */
export function costPerTestedGram(v: ProductVariant, testedProteinPer100g: number): number | null {
  const testedProtein = (v.net_weight_g * testedProteinPer100g) / 100;
  return testedProtein > 0 ? sellingPrice(v) / testedProtein : null;
}

/** Grams of protein you get for ₹100. Higher is better. */
export function proteinPer100Inr(v: ProductVariant): number | null {
  const cost = effectiveCostPerGram(v);
  return cost && cost > 0 ? 100 / cost : null;
}

/** Calories eaten per gram of protein (4 = pure protein). Lower is better. */
export function caloriesPerGramProtein(v: ProductVariant): number | null {
  return v.protein_g > 0 && v.calories_kcal > 0 ? v.calories_kcal / v.protein_g : null;
}

/** Grams of protein per 100 calories eaten (25 = pure protein). Higher is better. */
export function proteinPer100Calories(v: ProductVariant): number | null {
  return v.protein_g > 0 && v.calories_kcal > 0 ? (v.protein_g / v.calories_kcal) * 100 : null;
}

export type MetricKey =
  | "maxCostPerG"
  | "minProteinPer100"
  | "minProteinPer100Calories"
  | "maxCaloriesPerGProtein"
  | "minDensity";

export interface MetricRangeConfig {
  key: MetricKey;
  param: string;
  label: string;
  hint: string;
  min: number;
  max: number;
  step: number;
  /** "max" filters keep values at or below the slider, "min" filters keep values at or above it. */
  bound: "max" | "min";
  unit: string;
  value: (v: ProductVariant) => number | null;
}

export const METRIC_RANGES: MetricRangeConfig[] = [
  {
    key: "maxCostPerG",
    param: "max_cost",
    label: "Max ₹ per g protein",
    hint: "Best known price ÷ protein in pack",
    min: 1,
    max: 30,
    step: 0.5,
    bound: "max",
    unit: "₹/g",
    value: effectiveCostPerGram,
  },
  {
    key: "minProteinPer100",
    param: "min_p100",
    label: "Min protein per ₹100",
    hint: "Grams of protein your ₹100 buys",
    min: 0,
    max: 40,
    step: 1,
    bound: "min",
    unit: "g",
    value: proteinPer100Inr,
  },
  {
    key: "minProteinPer100Calories",
    param: "min_p100cal",
    label: "Min protein per 100 cal",
    hint: "25g = pure protein; higher is leaner",
    min: 0,
    max: 25,
    step: 1,
    bound: "min",
    unit: "g",
    value: proteinPer100Calories,
  },
  {
    key: "maxCaloriesPerGProtein",
    param: "max_kcal_pg",
    label: "Max calories per g protein",
    hint: "4 = pure protein; lower is leaner",
    min: 4,
    max: 30,
    step: 0.5,
    bound: "max",
    unit: "kcal",
    value: caloriesPerGramProtein,
  },
  {
    key: "minDensity",
    param: "min_density",
    label: "Min protein density",
    hint: "% of calories that come from protein",
    min: 0,
    max: 100,
    step: 5,
    bound: "min",
    unit: "%",
    value: (v) => v.protein_density_pct,
  },
];

/** True when the variant passes the range; variants missing the metric fail an active range. */
export function passesRange(config: MetricRangeConfig, v: ProductVariant, limit: number | undefined): boolean {
  if (limit === undefined) return true;
  const value = config.value(v);
  if (value === null) return false;
  return config.bound === "max" ? value <= limit : value >= limit;
}
