import type { ProductWithVariants } from "@/types/product";

/** 0 = no match, 1 = matched only in ingredients or protein source, 2 = matched the name, brand or variant. */
export type SearchRank = 0 | 1 | 2;

const ALIASES: Record<string, string> = {
  on: "optimum nutrition",
  mb: "muscleblaze",
  soya: "soy",
  yoghurt: "yogurt",
};

interface SearchIndex {
  primary: string;
  /** Primary text with spaces removed, so "wholetruth" finds "The Whole Truth". */
  primaryCompact: string;
  primaryWords: string[];
  secondary: string;
}

const indexes = new WeakMap<ProductWithVariants, SearchIndex>();

function normalize(text: string | null | undefined): string {
  return (text ?? "").toLowerCase().replace(/[^a-z0-9]+/g, " ").trim();
}

function indexOf(p: ProductWithVariants): SearchIndex {
  const cached = indexes.get(p);
  if (cached) return cached;
  const primary = normalize(
    [p.name, p.brand?.name, p.category?.name, ...p.variants.map((v) => v.variant_name)].join(" ")
  );
  const secondary = normalize(
    p.variants.flatMap((v) => [v.primary_protein_source ?? "", ...(v.ingredient_list ?? [])]).join(" ")
  );
  const index: SearchIndex = {
    primary,
    primaryCompact: primary.replace(/ /g, ""),
    primaryWords: [...new Set(primary.split(" "))],
    secondary,
  };
  indexes.set(p, index);
  return index;
}

/** Edit distance where swapping two neighbouring letters counts as one slip ("protien" vs "protein"). */
export function editDistance(a: string, b: string): number {
  const rows = Array.from({ length: a.length + 1 }, (_, i) => [i, ...new Array<number>(b.length).fill(0)]);
  for (let j = 0; j <= b.length; j++) rows[0][j] = j;
  for (let i = 1; i <= a.length; i++) {
    for (let j = 1; j <= b.length; j++) {
      const cost = a[i - 1] === b[j - 1] ? 0 : 1;
      rows[i][j] = Math.min(rows[i - 1][j] + 1, rows[i][j - 1] + 1, rows[i - 1][j - 1] + cost);
      if (i > 1 && j > 1 && a[i - 1] === b[j - 2] && a[i - 2] === b[j - 1]) {
        rows[i][j] = Math.min(rows[i][j], rows[i - 2][j - 2] + 1);
      }
    }
  }
  return rows[a.length][b.length];
}

function isCloseSpelling(term: string, words: string[]): boolean {
  if (term.length < 4) return false;
  const allowed = term.length >= 8 ? 2 : 1;
  return words.some((word) => Math.abs(word.length - term.length) <= allowed && editDistance(term, word) <= allowed);
}

function hasWord(text: string, term: string): boolean {
  return ` ${text} `.includes(` ${term} `);
}

/** Very short terms only count as whole words, otherwise "on" matches "protein". */
function matches(text: string, term: string): boolean {
  return term.length < 3 ? hasWord(text, term) : text.includes(term);
}

/** Every word of the query must be found, in any order; a typo in a word is allowed. */
export function searchRank(p: ProductWithVariants, query: string): SearchRank {
  const terms = normalize(query)
    .split(" ")
    .filter(Boolean)
    .flatMap((term) => (ALIASES[term] ?? term).split(" "));
  if (terms.length === 0) return 2;

  const index = indexOf(p);
  let rank: SearchRank = 2;
  for (const term of terms) {
    const inPrimary = matches(index.primary, term) || (term.length >= 3 && index.primaryCompact.includes(term));
    if (inPrimary) continue;
    if (matches(index.secondary, term)) {
      rank = 1;
      continue;
    }
    if (isCloseSpelling(term, index.primaryWords)) continue;
    return 0;
  }
  return rank;
}
