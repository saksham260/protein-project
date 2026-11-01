import type { ProductVariant, ProductWithVariants } from "@/types/product";
import { hasAllergenData } from "@/lib/allergens";
import { caloriesPerGramProtein, effectiveCostPerGram, proteinInPack, sellingPrice } from "@/lib/metrics";
import { computePer100g, formatPercentage, formatPrice, formatPricePerGram, formatWeight } from "@/lib/utils";

export const MAX_COMPARE = 4;

export interface CompareItem {
  key: string;
  product: ProductWithVariants;
  variant: ProductVariant;
}

/** Stable, readable id for one pack size. Mirrors how the uploader makes variant slugs unique. */
export function compareKey(product: { slug: string }, variant: { slug: string }): string {
  return variant.slug.startsWith(`${product.slug}-`) ? variant.slug : `${product.slug}-${variant.slug}`;
}

export function compareHref(keys: string[]): string {
  return keys.length > 0 ? `/compare?v=${keys.map(encodeURIComponent).join(",")}` : "/compare";
}

export function parseCompareKeys(param: string | null | undefined): string[] {
  const keys = (param ?? "").split(",").map((key) => key.trim()).filter(Boolean);
  return [...new Set(keys)].slice(0, MAX_COMPARE);
}

/** Keeps the order in the link, so a shared comparison looks the same to everyone. */
export function findCompareItems(catalog: ProductWithVariants[], keys: string[]): CompareItem[] {
  const byKey = new Map<string, CompareItem>();
  for (const product of catalog) {
    for (const variant of product.variants) {
      const key = compareKey(product, variant);
      byKey.set(key, { key, product, variant });
    }
  }
  return keys.flatMap((key) => {
    const item = byKey.get(key);
    return item ? [item] : [];
  });
}

export interface CompareNumberRow {
  kind: "number";
  label: string;
  value: (item: CompareItem) => number | null;
  format: (value: number | null) => string;
  /** Omitted when packs of different sizes can't fairly be ranked on this number. */
  better?: "lower" | "higher";
}

export interface CompareTextRow {
  kind: "text";
  label: string;
  value: (item: CompareItem) => string;
}

export type CompareRow = CompareNumberRow | CompareTextRow;

const per100g = (value: number, v: ProductVariant) => computePer100g(value, v.serving_size_g);
const grams = (value: number | null) => (value == null ? "—" : `${Number(value.toFixed(1))}g`);

function allergensText(v: ProductVariant): string {
  if (!hasAllergenData(v)) return "Info missing";
  const declared = [...new Set(v.allergens.map((a) => a.toLowerCase()))];
  return declared.length > 0 ? declared.join(", ") : "None declared";
}

function redFlagsText(v: ProductVariant): string {
  if (v.ingredient_list.length === 0) return "No ingredient list";
  const flags = v.red_flags ?? [];
  return flags.length > 0 ? flags.map((flag) => flag.flag_label).join(", ") : "None found";
}

export const COMPARE_ROWS: CompareRow[] = [
  { kind: "number", label: "Price", value: ({ variant }) => sellingPrice(variant), format: formatPrice },
  { kind: "number", label: "Pack size", value: ({ variant }) => variant.net_weight_g, format: formatWeight },
  {
    kind: "number",
    label: "Cost per gram of protein",
    value: ({ variant }) => effectiveCostPerGram(variant),
    format: formatPricePerGram,
    better: "lower",
  },
  {
    kind: "number",
    label: "Protein in pack",
    value: ({ variant }) => proteinInPack(variant),
    format: (value) => (value == null ? "—" : `${Math.round(value).toLocaleString("en-IN")}g`),
  },
  {
    kind: "number",
    label: "Protein per 100g",
    value: ({ variant }) => per100g(variant.protein_g, variant),
    format: grams,
    better: "higher",
  },
  {
    kind: "number",
    label: "Protein density",
    value: ({ variant }) => variant.protein_density_pct,
    format: formatPercentage,
    better: "higher",
  },
  {
    kind: "number",
    label: "Calories per g of protein",
    value: ({ variant }) => caloriesPerGramProtein(variant),
    format: (value) => (value == null ? "—" : `${value.toFixed(1)} kcal`),
    better: "lower",
  },
  {
    kind: "number",
    label: "Sugars per 100g",
    value: ({ variant }) => per100g(variant.total_sugars_g, variant),
    format: grams,
    better: "lower",
  },
  { kind: "text", label: "Main protein source", value: ({ variant }) => variant.primary_protein_source ?? "Not specified" },
  { kind: "text", label: "Tier", value: ({ variant }) => variant.protein_tier ?? "Unrated" },
  { kind: "text", label: "Label red flags", value: ({ variant }) => redFlagsText(variant) },
  { kind: "text", label: "Declared allergens", value: ({ variant }) => allergensText(variant) },
];

/** Which columns hold the best number in a row. Ties share it, and a row of equal values has no winner. */
export function bestColumns(row: CompareRow, items: CompareItem[]): Set<number> {
  if (row.kind === "text" || !row.better) return new Set();
  const values = items.map((item) => row.value(item));
  const known = values.filter((value): value is number => value !== null);
  if (known.length < 2 || new Set(known).size === 1) return new Set();
  const target = row.better === "lower" ? Math.min(...known) : Math.max(...known);
  return new Set(values.flatMap((value, index) => (value === target ? [index] : [])));
}
