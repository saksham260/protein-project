# Live pricing trial — 2026-11-09

All three approaches from `live-pricing-plan-2026-11-09.md` were run against the real brand stores in the catalog:
567 brand-store (D2C) links across 70 stores. The run was read-only: no database writes, one request per second per store.
Scripts and raw results are in `protein-etl/scratch/pricing_trial/`.

Amazon could not be tried under any approach. All 552 Amazon links are search links (`/s?k=`), with no product (`/dp/ASIN`) links, and there are no Creators API keys.

## Results

| | 1. Scheduled bulk poll | 2. On-demand live check | 3. Brand feeds |
|---|---|---|---|
| What ran | `/products.json` once per store (the repo's own poller code); product-page JSON-LD for stores without it | One request per product: `/products/<handle>.js` or the product page | Can't be pulled without the brands; measured as the gap left by 1 and 2 |
| Links priced live | **368 / 567 (65%)** | 113 / 196 sampled (58%) | — |
| Prices that differ from approach 1 | — | **0 of 113**: identical | — |
| Extra links priced vs approach 1 | — | **0** | the ~58 links on 7 brand sites that publish no price data |
| Cost | 219 requests, 5.4 min for all 70 stores | Shopify: p50 227 ms, p95 723 ms per product. Non-Shopify page: p50 299 ms, p95 1.2 s, ~124 KB | Outreach per brand |

### What approach 1 found
- **Most catalog prices are out of date.** Of the 368 prices it could read, 116 (32%) differ from the catalog: 71 cheaper, 45 dearer. The median change is 15%.
  - 48 changed by under 10%.
  - 38 changed by 10–50%.
  - 30 changed by more than 50%. The poller's safety check holds these back, and some look like variant mix-ups rather than real price moves.
- **105 variants are out of stock** on the brand's store but show as buyable on the site.
- 55 of 70 stores have the Shopify feed. Of the other 15 stores, the trial priced 40 of 126 links from the pages' JSON-LD. Nutrabay (24/24) and The Whole Truth (9/14) worked well.

### Why links were not priced (199)
| Cause | Links | Fix |
|---|---|---|
| Our variant name doesn't pick a store variant (e.g. "1kg Pouch" on a product with 8 flavours, no SKU) | 81 | One-time mapping: store the Shopify variant ID on each variant, then poll by ID |
| Product link is dead (product renamed or removed: 30 on Shopify stores, 28 elsewhere, incl. 4 to the placeholder host `unknown.com`) | 58 | Data cleanup: the site is sending people to broken pages today |
| Brand site loads but publishes no price data (Avvatar 17, Plix 16, Amul 15, Protinex 3, XLR8 3, others 4) | 58 | Approach 3 (ask for a feed), or a per-site page reader |
| Other (shared SKU, URL without a product path) | 2 | Manual |

## Verdict: approach 1 is the most suitable
1. **It does the job.** Coverage is 65% today and about 88% of live links once variant IDs are mapped and dead links removed, for 219 requests every few hours.
2. **Approach 2 adds no coverage.** It returned exactly the same prices as approach 1 and priced nothing approach 1 missed. Its only gain is freshness within the poll interval. One snapshot can't show intraday change, but most of the drift found here happened over weeks, so 6-hourly polling closes almost all of it. Revisit for sale days if click data shows it matters.
3. **Approach 3 is a targeted add-on, not the base.** About 58 links on 7 non-Shopify brands publish no machine-readable price. Amul, Avvatar and Plix make up 48 of them. Ask those brands for a feed, or write a small reader per site.

## Update: after building the two fixes (same day)
Steps 2 and 3 below are now built into the real poller (`src/pricing/d2c.py`, `src/pricing/pages.py`). It was re-run against the live stores, writing into an in-memory copy of the catalog (no Supabase): `scratch/pricing_trial/rerun_with_poller.py`.

| | Trial | Real poller with the fixes |
|---|---|---|
| Links priced and publishable | 338 (368 read, 30 held) | **348 / 567 (61%)** |
| Held back by the >50% check | 30 | 14 |
| Store variant IDs saved | — | 306 |
| Dead links reported | — | 25 |

**The ~88% estimate above was too optimistic.** Variant-ID matching mostly makes matches *safer* (fewer wrong-variant prices, fewer held prices) rather than adding many. The links still not priced (about 190):
- About 55 dead or renamed product links.
- 58 pages on 7 brand sites with no price data (Amul, Avvatar, Plix…).
- 26 links that point at the same store listing as another catalog variant. These are wrong links in our catalog, e.g. "Almond Fudge 60g" links to the coffee-crush bar page. They are skipped on purpose.
- About 32 links where the store sells several flavours at different prices and our variant name doesn't say which one. The poller does not guess.

Catalog SKUs can be wrong too. The Whole Truth "Light Cocoa 1kg" carries the 2 kg pack's SKU. The poller now ignores a SKU or saved ID whose pack size contradicts the variant name, and prices it at ₹4,119 (1 kg) rather than ₹8,219.

Realistic coverage after cleaning the dead and wrong links is about 75–80%. Reaching more needs brand feeds or hand-mapping of the flavour cases.

## Next steps, in order
1. Clean the dead D2C links (and `unknown.com`) and the 26 wrong shared links.
2. ~~One-time variant mapping~~ Built: the poller saves and matches by store variant ID automatically on its first run.
3. ~~Add the JSON-LD reader~~ Built.
4. Run migration 016, do one poll by hand with `dry_run`, then turn on the 6-hourly schedule.
5. Contact Amul, Avvatar and Plix for feeds.
6. Amazon: replace search links with `/dp/ASIN` links before the Creators API job can do anything.
