# Feature Build Walkthrough (2026-11-01)

Builds the "Now" features from [feature-research-2026-11-01.md](feature-research-2026-11-01.md), on top of the audit fixes in [audit-fixes-walkthrough.md](audit-fixes-walkthrough.md). Work is on the branch `audit-fixes`, uncommitted.

## What was built

| Research item | What it is | Where |
|---|---|---|
| 4. Compare page | Up to 4 products side by side, with the better number in each row marked, and a link to share. Open it from the cart. | `/compare`, [compare.ts](../protein-web/src/lib/compare.ts) |
| 5. Value leaderboards | 6 ranked lists, such as lowest-cost whey isolate and protein bars without maltitol. | `/best`, [bestLists.ts](../protein-web/src/lib/bestLists.ts) |
| 8. Protein planner (first part) | Cost per day and per month for a daily amount of protein, filtered by form and diet. | `/protein-cost-calculator`, [proteinCost.ts](../protein-web/src/lib/proteinCost.ts) |
| 6. "Is this genuine?" (phase 1) | General steps on each product page, with a link to the FSSAI licence lookup and the brand's store. | [GenuineCheckCard.tsx](../protein-web/src/components/product/GenuineCheckCard.tsx) |
| 3. Lab evidence panel | Shows published test reports on the product page. Says so plainly when there are none. | [LabReportPanel.tsx](../protein-web/src/components/product/LabReportPanel.tsx), migration 015 |

Footer links, the sitemap and the how-we-rate page were updated to match. The compare page is hidden from search engines, because every link is a different mix of products. The leaderboards are meant to be found.

## What you need to do

1. **Add migration 015 to the list.** Run these in the Supabase SQL editor, in order: 008, 010, 012, 014, 015. Product pages work without 015, and simply show that no report is on file.
2. **Fix 6 wrong MRPs in the live database.** Each has an MRP below the brand's own store price, which can't be right because MRP is the legal maximum. The list is below. The site now labels those as "Price" instead of "MRP", but the MRP sort is still wrong for them.
3. **Add lab reports.** The panel is empty until you do. See below.
4. **Run the tests**, as in the audit walkthrough. `src/lib/features.test.ts` is new and unrun.
5. **Check the pages by eye**, especially the compare table on a phone.

### Variants with an MRP below their store price

| Product | Pack | MRP in database | Store price |
|---|---|---|---|
| Pintola High Protein Peanut Butter Dark Chocolate | 510g | ₹355 | ₹499 |
| MyFitness High Protein Peanut Butter Crispy Dark Chocolate | 510g | ₹319 | ₹549 |
| The Whole Truth Plant Protein Double Cocoa | 1kg | ₹1,425 | ₹2,699 |
| The Whole Truth Plant Protein Pista Badaam | 1kg | ₹1,575 | ₹2,799 |
| Optimum Nutrition Gold Standard Vanilla Ice Cream | 907g | ₹3,449 | ₹3,899 |
| OZiva Organic Plant Protein | 500g | ₹1,329 | ₹1,349 |

₹/g rankings aren't affected, because they use store prices when known.

### Adding a lab report

In the Supabase table editor, add a row to `test_reports`:

| Field | Meaning |
|---|---|
| `product_id` | The product |
| `variant_id` | Optional: the pack, if the report covers only one |
| `source_type` | `independent` or `brand` |
| `source_name` | Who published it |
| `lab_name`, `batch_number` | Optional, but show them when known |
| `tested_on` | Test date |
| `result` | `pass`, `partial` or `fail`, as the report itself says |
| `tested_protein_g_per_100g` | Optional. The page then shows ₹/g on tested protein. |
| `report_url` | Link to the original report. Must start with `https://`. |

Link to reports rather than copying them, and ask Trustified and Unbox for permission before listing their results. Have a lawyer look at this before publishing any "fail".

## Checked against the real catalog

Each feature's real code was run over the live catalog (379 products, 489 variants).

- All 6 lists fill: 10 products each, 9 for peanut butter.
- All 489 compare links are unique.
- The checks caught two real problems, both now handled:
  - The "Whey Isolate" list ranked Titan Whey first, at only 64% protein, because the catalog's source field names a blend's first protein. Blends are now ruled out.
  - The 6 wrong MRPs above.
- A Biozyme, Biozyme Iso and Gold Standard comparison gave sensible figures.

## Facts checked at the source

| Fact on the site | Status |
|---|---|
| ICMR-NIN: 0.83 g/kg/day, or 1 g/kg on cereal-based diets | Confirmed in the [NIN brief note](https://www.nin.res.in/rdabook/brief_note.pdf) |
| ICMR-NIN 2024: healthy people advised against protein supplements | News reports only, so the page says "were reported as". Replace the link with the guidelines themselves if you can. |
| FoSCoS is the licence lookup, with a 14-digit number | The [site](https://foscos.fssai.gov.in/) exists; the steps and digit count come from several third-party guides |

## Not built, and why

| Research item | Reason |
|---|---|
| 7. Claim Check | **Held back on purpose.** FSSAI's thresholds couldn't be confirmed: the [2019 direction](https://www.fssai.gov.in/upload/advisories/2019/06/5d164a5daa382Direction_Advertising_Claims_28_06_2019.pdf) on its site is a cover letter without them, and the compendium link was dead. Publishing "fails FSSAI's level" on an unverified number could wrongly accuse a brand. It needs the gazette text. |
| 6. Genuine card, phase 2 | Needs Amazon seller data. `official_sellers.json` wasn't used, because nothing shows where its seller lists came from. |
| 8. Planner quiz | Needs a qualified reviewer, as it moves from arithmetic to recommendations. |
| 9. Send to Amazon cart | Needs real ASINs. |
| 10. Partner links | Needs you to join the affiliate programmes. |
| 11. Refill reminders | Needs an email provider and a consent flow. |
| 12. Sub-scores | Needs lab data to mean anything. |
| 13. Diet clarity fields | Needs rennet, lactose and Jain facts gathered by hand. |
| 14. Ratings, 15. Test fund | Marked "Later" in the research. Both need traffic first. |

Also left out: a preview image for shared compare links, and a "has lab report" filter, which should wait until there are reports to filter.
