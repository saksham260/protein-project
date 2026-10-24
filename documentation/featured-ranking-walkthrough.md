# "Featured" display order (bundles low, bigger brands high)

Date: 2026-10-24

## What changed
Product lists (home, categories, explore, search) now open in a new default order called **Featured**:
1. **Individual items** first, then **multi-packs** of the same item, then **combos / bundles / free-gift deals** last.
2. Inside each of those groups, **bigger, better-known brands** first.
3. Then the lowest cost per gram of protein.

Choosing any other option in the sort dropdown (cheapest protein, density, price...) uses that sort only. The Top Picks awards always use cost per gram, so they are unchanged. The dropdown's first option is now "Featured — Popular brands first".

## How a product is classed
Defined in `protein-web/src/lib/ranking.ts` from the product name, the variant name and the `is_combo` flag:
- **Combo / bundle (lowest):** `is_combo`, or the words combo, bundle, variety, assorted, sampler, hamper, starter kit, trial pack, or "+ free ...".
- **Multi-pack (middle):** "Pack of N", "Box of N", "Case/Carton/Set of N" (N of 2 or more), "N Packs", "multipack". "Box of N sachets" does **not** count (that is how sachet products are sold).
- **Individual (highest):** everything else.

Current catalog split (280 products): 212 individual, 66 multi-packs, 2 combos (both Scitron).

## Brand order
`BRAND_TIERS` in `ranking.ts` (edit the lists to change it; names ignore upper/lower case):
- **Tier 1 (household names):** MuscleBlaze, Optimum Nutrition, Isopure, GNC India, Amul, Yoga Bar, The Whole Truth, Fast&Up, Max Protein, RiteBite Max Protein, MyFitness, Pintola, Epigamia, Bagrry's.
- **Tier 2 (well known):** Avvatar, Beastlife, Wellbeing Nutrition, Muscle Nectar, Nutrabay, Chase, SuperYou, Alpino, Open Secret, True Elements, Sleepy Owl, Plix, Kapiva, Nakpro, Phab, Naturaltein, One Science Nutrition, AS-IT-IS Nutrition, Bolt Nutrition, Scitron, Eat Anytime, Bigmuscles Nutrition, XLR8 Sports Nutrition, Origin Nutrition.
- **Tier 3:** every other brand, including new ones.

These tiers are a judgment call, not sales data. Review and adjust them.

## Files
| File | Change |
|---|---|
| `src/lib/ranking.ts` | New. `bundleLevel`, `brandTier`, `featuredScore` |
| `src/lib/data.ts` | New `featured` sort; it is now the default |
| `src/lib/constants.ts`, `src/hooks/useFilters.ts`, `src/components/search/SortDropdown.tsx` | "Featured" added and made the default (it is left out of the URL when selected) |
| `src/lib/ranking.test.ts`, `src/lib/data.test.ts` | Tests for the classes, the brand tiers and the default order |

## Known effect
Within a tier, products are ordered by cost per gram, so a brand with many cheap products (e.g. Max Protein, 25 items) can fill the first screen of a list. If you want brands mixed instead, that needs an interleaving step.
