import type { ProductVariant } from "@/types/product";
import { canonicalDietaryTag } from "@/lib/utils";

// Corrections applied to every variant as it is loaded, so the live database and the seed catalog read the same.

const GLYCEMIC_POLYOLS = /\b(maltitol|sorbitol|xylitol|isomalt|lactitol|mannitol|hydrogenated glucose syrup|ins 965)\b/;
const POLYOL_NAMES = ["maltitol", "sorbitol", "xylitol", "isomalt", "lactitol", "mannitol", "erythritol"];
const SUGAR_DENIALS = /sugar[- ]?free|no added sugar|no sugar|without sugar|sugar alcohol|sugar substitute/g;
const ADDED_SUGARS =
  /(?<![a-z-])(sugar|jaggery|gur|honey|glucose|dextrose|fructose|corn syrup|invert syrup|date syrup|rice syrup|maple syrup)\b/;
const NOT_VEGETARIAN = /\b(eggs?|albumen|gelatine?|collagen)\b/;

function ingredientText(v: Pick<ProductVariant, "ingredient_list">): string {
  return (v.ingredient_list ?? []).join(" , ").toLowerCase();
}

/** The sweeteners behind the polyol figure, as named on the ingredient list. */
export function polyolLabel(v: Pick<ProductVariant, "ingredient_list">): string {
  const text = ingredientText(v);
  const named = POLYOL_NAMES.filter((name) => text.includes(name));
  if (text.includes("ins 965") && !named.includes("maltitol")) named.unshift("maltitol");
  if (named.length === 0) return "Polyols";
  return `Polyols (${named.map((n) => n[0].toUpperCase() + n.slice(1)).join(", ")})`;
}

/** Only sweeteners the body barely absorbs come off net carbs; maltitol and friends still raise blood sugar. */
export function correctedNetCarbs(
  v: Pick<
    ProductVariant,
    "ingredient_list" | "total_carbs_g" | "dietary_fiber_g" | "non_glycemic_polyols_g" | "true_net_carbs_g"
  >
): number | null {
  if (!v.non_glycemic_polyols_g || !GLYCEMIC_POLYOLS.test(ingredientText(v))) return v.true_net_carbs_g;
  return Number(Math.max(0, v.total_carbs_g - v.dietary_fiber_g).toFixed(2));
}

/** Canonical tags, minus any the variant's own label contradicts. */
export function cleanDietaryTags(
  v: Pick<ProductVariant, "dietary_tags" | "ingredient_list" | "added_sugars_g">
): string[] {
  const text = ingredientText(v);
  const hasAddedSugar = (v.added_sugars_g ?? 0) > 0 || ADDED_SUGARS.test(text.replace(SUGAR_DENIALS, " "));
  const tags = (v.dietary_tags ?? []).map(canonicalDietaryTag);
  return [...new Set(tags)].filter((tag) => {
    if (tag === "no-added-sugar") return !hasAddedSugar;
    if (tag === "vegetarian") return !NOT_VEGETARIAN.test(text);
    return Boolean(tag);
  });
}

export function normalizeVariantFacts<T extends ProductVariant>(v: T): T {
  return { ...v, dietary_tags: cleanDietaryTags(v), true_net_carbs_g: correctedNetCarbs(v) };
}
