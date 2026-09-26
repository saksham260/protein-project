import { ProductVariant } from "@/types/product";

// Derived protein metrics. Formulas are documented in documentation/phase3-pricing-metrics-location-plan.md.

/** ₹ per gram of protein at the best known price, falling back to MRP. Lower is better. */
export function effectiveCostPerGram(v: ProductVariant): number | null {
  return v.best_cost_per_g_protein ?? v.cost_per_g_protein ?? null;
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

export type MetricKey = "maxCostPerG" | "minProteinPer100" | "maxCaloriesPerGProtein" | "minDensity";

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
