# phase-2-raw: missing `src/lib` + local stand-ins

**Date:** 2026-09-15
**Branch:** `phase-2-raw` (pulled from `origin/phase-2-raw`, HEAD `027c478`)

## Problem
`protein-web` would not start. Every page failed with a 500 error:
`Module not found: Can't resolve '@/lib/utils' | '@/lib/constants' | '@/lib/data'`.

**Root cause:** line 14 of the root `.gitignore` is `lib/`. It's a Python-template rule, and it also
matches `protein-web/src/lib/`. So the author's `src/lib` folder was never committed or pushed.
(`git check-ignore -v protein-web/src/lib/utils.ts` → `.gitignore:14:lib/`)

**Permanent fix (for the branch owner):** change the rule to `/lib/`, or add `!protein-web/src/lib/`,
then commit the real `src/lib` files.

## What was done locally (not committed)
I wrote four stand-in files so the UI could be previewed. They are rebuilt from how the components
use them and from `.planning/phases/02-*/02-0{1,2}-PLAN.md` + `implementation_plan.md` §6.3.
Each one has a `LOCAL STAND-IN` header comment. They stay git-ignored by the same `lib/` rule,
so they can't be committed by accident.

| File | Exports | Notes |
|---|---|---|
| `src/lib/utils.ts` | `cn`, `formatPrice`, `formatPricePerGram`, `formatPercentage`, `formatWeight`, `computePer100g` | Returns `—` for null values |
| `src/lib/constants.ts` | `CATEGORIES`, `PROTEIN_TIERS`, `SORT_OPTIONS`, `ALLERGENS_LIST`, `DIETARY_TAGS_LIST`, `PLATFORM_INFO` | Category descriptions and icons are my own placeholders |
| `src/lib/redirect.ts` | `buildRedirectUrl`, `getPriceDisplay` | Follows plan §6.3. Quick-commerce apps (Blinkit, Zepto, Instamart) always show "check local price" |
| `src/lib/data.ts` | `getProducts(filters)`, `getProductBySlug`, `QueryFilters` | **Seed-only.** Reads `src/data/seedCatalog.json`. Supports filters (category, tier, tags, allergen exclusion, zero-flags), search and 5 sorts. The original reportedly used Supabase with a seed fallback |

Data-mapping detail: seed tiers look like `"Tier 1 – Premium Isolate/Hydrolysate"`. They are normalised
to `"Tier 1"` so they match the `PROTEIN_TIERS` keys and the tier filter.

Not recreated: `src/lib/supabase/{client,server}.ts`. No component imports them in this branch.

## Dev-server setup
- Added a `protein-web` entry (port 3000) to `C:\development\.claude\launch.json`.
- No `.env.local` exists. The app runs without Supabase because `middleware.ts` skips auth when the keys are missing.

## Verification
- `npx tsc --noEmit` passes.
- Checked in the browser: `/` (hero, categories, cost-efficiency leaderboard), `/explore` (filters + grid),
  `/product/amul-high-protein-buttermilk` (metrics, buy links, nutrition panel).

## Update: `phase2ui` branch
`origin/phase2ui` is the exact same commit as `phase-2-raw` (`027c478`), so it has the same missing `src/lib`
and the same `.gitignore` rule. I checked it out locally as `phase2ui`. The stand-ins above are still in use.

## Resolved (2026-09-15)
Saksham pushed `ec39276` "fix(web): unignore and include protein-web/src/lib in repository" to `phase2ui`.
It changes `.gitignore` to `/lib/` and adds the real `src/lib/{utils,constants,data,redirect}.ts` + `src/lib/supabase/{client,server}.ts`.
I deleted the stand-ins and fast-forwarded. `tsc --noEmit` passes, and `/`, `/explore` (all 15 cards) and product pages return 200.
The stand-ins described above no longer exist.

## When the real files arrive
Delete `protein-web/src/lib/` and pull. The real versions replace these stand-ins completely.
