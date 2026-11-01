import type { ProductVariant } from "@/types/product";

export type AllergenGroup = "milk" | "soy" | "gluten" | "tree_nuts" | "peanuts" | "eggs";

/**
 * Allergens are free text in the data ("Almonds", "nuts", "egg"), so every word a label might use is
 * mapped to the filter groups it belongs to. "nuts" alone doesn't say which nuts, so it counts as both.
 * Oats sit under gluten because they are often cross-contaminated.
 */
const GROUPS_BY_WORD: Record<string, AllergenGroup[]> = {
  milk: ["milk"],
  dairy: ["milk"],
  whey: ["milk"],
  lactose: ["milk"],
  casein: ["milk"],
  soy: ["soy"],
  soya: ["soy"],
  soybean: ["soy"],
  soybeans: ["soy"],
  gluten: ["gluten"],
  wheat: ["gluten"],
  barley: ["gluten"],
  rye: ["gluten"],
  oat: ["gluten"],
  oats: ["gluten"],
  nut: ["tree_nuts", "peanuts"],
  nuts: ["tree_nuts", "peanuts"],
  "tree nut": ["tree_nuts"],
  "tree nuts": ["tree_nuts"],
  almond: ["tree_nuts"],
  almonds: ["tree_nuts"],
  cashew: ["tree_nuts"],
  cashews: ["tree_nuts"],
  walnut: ["tree_nuts"],
  walnuts: ["tree_nuts"],
  pistachio: ["tree_nuts"],
  pistachios: ["tree_nuts"],
  hazelnut: ["tree_nuts"],
  hazelnuts: ["tree_nuts"],
  pecan: ["tree_nuts"],
  pecans: ["tree_nuts"],
  macadamia: ["tree_nuts"],
  peanut: ["peanuts"],
  peanuts: ["peanuts"],
  groundnut: ["peanuts"],
  groundnuts: ["peanuts"],
  egg: ["eggs"],
  eggs: ["eggs"],
};

/** Backstop for items the label's allergen list missed. Plant milks and nut butters are not dairy. */
const INGREDIENT_PATTERNS: Record<AllergenGroup, RegExp> = {
  milk: /\b(whey|casein|caseinate|lactose|ghee|paneer|curd|yogh?urt|(?<!coconut |almond |oat |soy |soya |rice |cashew |peanut )milk)\b/,
  soy: /\b(soy|soya|soybean|soybeans)\b/,
  gluten: /\b(wheat|atta|maida|gluten|barley|rye|semolina|suji|oat|oats)\b/,
  tree_nuts: /\b(almonds?|cashews?|walnuts?|pistachios?|hazelnuts?|pecans?|macadamias?|badam|kaju|pista)\b/,
  peanuts: /\b(peanuts?|groundnuts?)\b/,
  eggs: /\b(eggs?|albumen|albumin)\b/,
};

export function allergenGroups(word: string): AllergenGroup[] {
  return GROUPS_BY_WORD[word.trim().toLowerCase().replace(/_/g, " ")] ?? [];
}

/** Which groups this variant contains, from its declared allergens and its ingredient list. */
export function variantAllergenGroups(v: Pick<ProductVariant, "allergens" | "ingredient_list">): Set<AllergenGroup> {
  const groups = new Set<AllergenGroup>((v.allergens ?? []).flatMap(allergenGroups));
  const ingredients = (v.ingredient_list ?? []).join(" , ").toLowerCase();
  for (const [group, pattern] of Object.entries(INGREDIENT_PATTERNS) as [AllergenGroup, RegExp][]) {
    if (pattern.test(ingredients)) groups.add(group);
  }
  return groups;
}

/** False when the label gave us nothing to judge by, which is not the same as "contains no allergens". */
export function hasAllergenData(v: Pick<ProductVariant, "allergens" | "ingredient_list">): boolean {
  return (v.allergens ?? []).length > 0 || (v.ingredient_list ?? []).length > 0;
}

/** Keeps a variant only when it is known to be free of every excluded group. */
export function passesAllergenExclusions(
  v: Pick<ProductVariant, "allergens" | "ingredient_list">,
  excluded: string[] | undefined
): boolean {
  if (!excluded?.length) return true;
  if (!hasAllergenData(v)) return false;
  const groups = variantAllergenGroups(v);
  return excluded.every((value) => allergenGroups(value).every((group) => !groups.has(group)));
}
