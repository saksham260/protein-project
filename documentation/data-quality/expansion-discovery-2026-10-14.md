# Phase 0 Catalog Expansion Discovery Report

**Date:** 2026-10-14  
**Status:** Ready for User Review & Approval  
**Target:** 64 proposed items across Batch 1 (New Brands) and Batch 2 (Existing Brand Gaps)  

---

## 1. Resolution of 404 Handles (Action Required)

During pre-flight validation, 2 handles returned HTTP 404:

### A. Scitron `advance-whey-protein` (scitron.com)
- **Status:** 404 Not Found on official store.
- **Store Audit:** Scitron has discontinued the standalone Advance Whey product page. Active whey protein product lines currently on `scitron.com` are:
  1. `buy-nitro-series-super-whey-isolate` (Already in proposed batch)
  2. `buy-ripped-whey-protein` (Already in proposed batch)
  3. `buy-nitro-series-performance-whey-protein` (Already in proposed batch)
  4. `scitron-advance-whey-1kg-kulfi-with-scitron-advance-bcaa-variety-flavor-variety-pack` (Combo: 1kg Kulfi + Advance BCAA Variety Pack @ ₹3,649)
- **Recommendation:**
  - **Option 1 (Recommended):** Drop the missing standalone handle and proceed with Scitron's 3 flagship active whey lines (Super Whey Isolate, Ripped Whey, Performance Whey).
  - **Option 2:** List the Advance Whey Kulfi Combo (`scitron-advance-whey-1kg-kulfi-with-scitron-advance-bcaa-variety-flavor-variety-pack`) marked as `(Combo)`.

### B. AS-IT-IS `atom-whey-protein-xl-with-digezyme-fermented-yeast-protein` (asitisnutrition.com)
- **Status:** 404 with plain ASCII handle because the live Shopify store uses the registered trademark symbol `®` (`atom-whey-protein-xl-with-digezyme®-fermented-yeast-protein`).
- **Store Audit:** AS-IT-IS has two relevant active flagship whey handles:
  1. `atom-whey-protein` — **Flagship AS-IT-IS ATOM Whey Protein | 27g Protein per Serving | DigeZyme Enzymes & 1B CFU Probiotics** (Price: ₹3,299 / 1kg). Clean URL, widely consumed flagship.
  2. `atom-whey-protein-xl-with-digezyme®-fermented-yeast-protein` — ATOM Whey Protein XL (Price: ₹2,471).
- **Recommendation:**
  - **Recommended:** Replace with `atom-whey-protein` (`https://asitisnutrition.com/products/atom-whey-protein`). Cleanest handle, most popular flagship ATOM whey in India.

---

## 2. Pack Products & Single-Unit Availability Audit

Per Rule A3 and User Decision Q1, we audited the brand stores for individual single units for each pack product:

| Brand | Proposed Product | Pack Sizes on Store | Single Unit on Brand Store? | Implementation Action |
|---|---|---|---|---|
| **Phab** | 21g Protein Bar (Chocolate Brownie) | Pack of 12 (₹1,500), Pack of 24, Pack of 72 | **None** (Store sells boxes only) | Listing: `Pack of 12` default, `Pack of 24/72` variants. Note: *No single available*. |
| **Phab** | 21g Protein Bar (Mocha Nut Fudge) | Pack of 12 (₹1,500), Pack of 24, Pack of 72 | **None** (Store sells boxes only) | Listing: `Pack of 12` default, `Pack of 24/72` variants. Note: *No single available*. |
| **Phab** | 10g Millet Wafer Bar (Lemon Pie) | Pack of 10 (₹700), Pack of 20, Pack of 30 | **None** (Store sells boxes only) | Listing: `Pack of 10` default, `Pack of 20/30` variants. Note: *No single available*. |
| **Phab** | 10g Millet Wafer Bar (Cookies & Cream) | Pack of 10 (₹700), Pack of 20, Pack of 30 | **None** (Store sells boxes only) | Listing: `Pack of 10` default, `Pack of 20/30` variants. Note: *No single available*. |
| **Phab** | 18g Milkshake (Cold Coffee) | Pack of 6 (₹750), Pack of 12, Pack of 18 | **None** (Store sells packs only) | Listing: `Pack of 6` default, `Pack of 12/18` variants. Note: *No single available*. |
| **Phab** | 18g Milkshake (Strawberries & Cream) | Pack of 6 (₹750), Pack of 12, Pack of 24 | **None** (Store sells packs only) | Listing: `Pack of 6` default, `Pack of 12/24` variants. Note: *No single available*. |
| **Phab** | 18g Milkshake (Classic Chocolate) | Pack of 6 (₹750), Pack of 12, Pack of 24 | **None** (Store sells packs only) | Listing: `Pack of 6` default, `Pack of 12/24` variants. Note: *No single available*. |
| **Cosmix** | Choco Peanut Protein Bar | Pack of 6 (270g, ₹420) | **None** (Store sells boxes only) | Listing: `Pack of 6` default. Note: *No single available*. |
| **Yoga Bar** | Power Up Coffee 20g Protein Bar | Pack of 5 (350g, ₹375) | **None** (Store sells packs only) | Listing: `Pack of 5` default. Note: *No single available*. |
| **Yoga Bar** | 26g Protein Shake Double Choc | Pack of 6 (₹699), Pack of 24, Pack of 30 | **None** (Store sells packs only) | Update existing listing with `Pack of 24` & `Pack of 30` variants. |
| **Muscle Nectar** | Protein Almonds Bar (Sea Salt) | 6 Bars (180g, ₹399) | **None** (Store sells boxes only) | Listing: `Pack of 6` default. Note: *No single available*. |
| **AS-IT-IS** | ATOM Whey Sachets Assorted | Pack of 6 (36g each, ₹699) | **None** (Store sells packs only) | Listing: `Pack of 6` default. Note: *No single available*. |
| **Optimum Nutrition** | Gold Standard Whey Vanilla Sachets | Pack of 5 (₹999) | **None** (Store sells packs only) | Listing: `Pack of 5` default. Note: *No single available*. |
| **Alpino** | Super Bar Chocolate 40g | 40g single (₹70), Pack of 10 (₹599) | **Found** (`super-bar-chocolate-40g` @ ₹70) | Single bar variant (₹70) + Pack of 10 (₹599) on same listing. |
| **Alpino** | Super Bar Cookies n' Cream | Pack of 10 (₹599) | **None** (`super-bar-cookies-n-cream-40g` is 404) | Listing: `Pack of 10` default. Note: *No single available*. |

---

## 3. Flavour Merging & Sibling Flavour Discovery

Per User Decisions A6, F1, and G2, flavour siblings of the same product line will be merged into a single multi-variant listing.

### A. Optimum Nutrition Gold Standard 100% Whey
- **Core Product Listing:** `Optimum Nutrition Gold Standard 100% Whey Protein`
- **Flavours Discovered on Store:**
  1. *Double Rich Chocolate* (Sizes: 1 lbs, 2 lbs / 907g, 5 lbs, 1.7 kg, 4 kg)
  2. *Vanilla Ice Cream* (Sizes: 1 lbs, 2 lbs, 5 lbs, 4 kg)
  3. *Unflavoured* (Size: 2 lbs / 907g)
  4. *Alphonso Mango* (Sizes: 2 lbs, 5 lbs, 1.7 kg, 4 kg)
  5. *Pack of 5 Sachets* (Vanilla Ice Cream, Alphonso Mango)
- **Variant Budget & Priority (Max 12 variants cap per F3/G1):**
  - Slot 1: Double Rich Chocolate (907g / 2 lbs) — **Default**
  - Slot 2: Vanilla Ice Cream (907g / 2 lbs)
  - Slot 3: Unflavoured (907g / 2 lbs)
  - Slot 4: Alphonso Mango (907g / 2 lbs)
  - Slot 5: Double Rich Chocolate (5 lbs / 2.27kg)
  - Slot 6: Vanilla Ice Cream (5 lbs / 2.27kg)
  - Slot 7: Double Rich Chocolate (1 lbs / 454g)
  - Slot 8: Vanilla Ice Cream (1 lbs / 454g)
  - Slot 9: Double Rich Chocolate (4 kg)
  - Slot 10: Vanilla Ice Cream (4 kg)
  - Slot 11: Vanilla Ice Cream (Pack of 5 Sachets)
  - Slot 12: Alphonso Mango (Pack of 5 Sachets)
  - *Combos with multivitamin/ZMA/creatine dropped to fit 12-variant cap.*

### B. Phab 18g Protein Milkshakes
- **Core Product Listing:** `Phab 18g Protein Milkshake`
- **Merged Flavours:**
  1. *Cold Coffee* (Pack of 6, Pack of 12, Pack of 18)
  2. *Strawberries & Cream* (Pack of 6, Pack of 12, Pack of 24)
  3. *Classic Chocolate* (Pack of 6, Pack of 12, Pack of 24)
- **Variant Allocation:** 3 flavours × 3 pack sizes = 9 variants (all within 12 cap).

### C. Cosmix No-Nonsense Plant Protein Pro
- **Core Product Listing:** `Cosmix No-Nonsense Plant Protein Pro`
- **Merged Flavours:**
  1. *Classic Unflavoured* (500g, 1kg)
  2. *Kerala Vanilla Bean* (500g, 1kg)
  3. *Malnad Arabica Coffee* (500g, 1kg)
- **Variant Allocation:** 3 flavours × 2 sizes = 6 variants (all within 12 cap).

### D. Fast&Up Plant Protein
- **Core Product Listing:** `Fast&Up Plant Protein`
- **Merged Flavours:**
  1. *Alphonso Mango* (1kg)
  2. *Cookies & Cream* (1kg + Shaker Combo)
- Plus standalone `Fast&Up Yeast Protein` listing (Unflavoured 1kg, Coffee 1kg).

---

## 4. Category Re-classification: `breakfast-cereals` (🥣)

Per User Decisions A8 and F7, the following 5 products will be assigned/moved to the new `breakfast-cereals` category:
1. `GNC High Protein Oats Dark Bliss (Chocolate)` (New addition from Batch 1)
2. `Chase Tomato Blast 20g Protein Puffs` -> Remains in `savory-snacks`
3. `Chase Mango Flavoured 20g Protein Cereal (Pack of 8)` -> **Moved** from `savory-snacks` to `breakfast-cereals`
4. `Chase Tiramisu 20g Protein Cereal (Pack of 8)` -> **Moved** from `savory-snacks` to `breakfast-cereals`
5. `Chase Choco Bites 20g Protein Cereal (Pack of 8)` -> **Moved** from `savory-snacks` to `breakfast-cereals`
6. `Yoga Bar High Protein Oats Crisps` -> **Moved** from `savory-snacks` to `breakfast-cereals`

---

## 5. Next Steps Pending Your Approval
1. Approve the 404 replacements: Drop Scitron `advance-whey-protein` (keep the 3 active whey lines) and replace AS-IT-IS with clean `atom-whey-protein`.
2. Confirm the single-unit audit findings (only Alpino chocolate bar has a single unit; all others will display pack options with 'no single available').
3. Once approved, proceed immediately with **Phase 1: Pipeline & Database Migration Setup**.