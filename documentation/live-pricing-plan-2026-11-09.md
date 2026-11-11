# Plan — Live pricing instead of scraped snapshots

Date: 2026-11-09 · Status: proposal

## Where we are
Most of the machinery already exists. It just isn't switched on:
- `src/pricing/d2c.py` reads each brand's public Shopify `/products.json`, matches variants by SKU, then by name, and writes price, stock, check time and history. Its workflow `poll-d2c-prices.yml` has the **schedule commented out**.
- `src/pricing/amazon.py` already uses the **Creators API**, which replaced PA-API 5 in 2026. Its workflow `poll-prices.yml` is also unscheduled, and Amazon links are still search links (`/s?k=`), so it can't match anything.
- So every price on the site is a snapshot from when the catalog was scraped. The upload scripts then stamped those snapshots "checked now" (fixed today; see `data-quality/2026-11-09-data-incident.md`).

**One rule for every approach:** a price is stored with the time it was **actually read** and its source. The site shows its age and never treats an unknown-age price as current.

---

## Approach 1 — Scheduled polling of official sources ("merchant feed" model)
Poll each source on a timer, staying inside the age limits the UI already enforces (Amazon 24 h, brand store 14 days).

| Source | How | Covers |
|---|---|---|
| Shopify brand stores | `/products.json` (built) | Most of the catalog. 254 of 476 product images are on `cdn.shopify.com`, a rough measure of Shopify brands. |
| Amazon.in | Creators API `getItems` with `offersV2` (built) | Products with an ASIN link |
| Non-Shopify brand sites (Amul, Protinex, Avvatar…) | **New:** read the `schema.org/Product` → `Offer` (price, availability) JSON-LD on the product page | Brands whose pages carry structured data |

Frequency by popularity: top ~50 viewed products hourly, the rest every 6 h. Amazon must stay under 24 h.

**Who does this:** Google Shopping. Merchants submit feeds, and Google also crawls the landing pages' structured data to correct price and availability itself ("automatic item updates"). Google notes the markup must be in the server HTML, and that this doesn't replace regular feed updates. Keepa and CamelCamelCamel run the same scheduled model against Amazon.

- ✅ Mostly built. Cheap (GitHub Actions). Legal: official feeds, API or public markup, at a polite rate.
- ❌ Prices are up to one poll interval old. Each non-Shopify site needs its markup checked. Amazon needs Associates eligibility (sales threshold) for API access.

## Approach 2 — Cache, plus a live check when someone looks ("Skyscanner" model)
Keep Approach 1's cache. When a product page is opened and its price is older than a short TTL (e.g. 30 min), fetch **just that variant** live in the background and update the page (stale-while-revalidate).
- Shopify: `GET https://<store>/products/<handle>.js`, one small request.
- Amazon: Creators API `getItems` for one ASIN.
- Run it in a Next route handler or a Supabase Edge Function. Lock per variant (at most one refresh per TTL) so traffic can't hammer a store.
- Optional: re-check on "Buy" click and show "price changed" if it moved.

**Who does this:** Skyscanner. Its browse cache holds prices from earlier searches (kept up to 15 days; indicative prices can be ~4 days old). A specific search triggers live quotes from suppliers, which can take up to a minute. For partner caches, a cached quote older than the set TTL triggers a live call.

- ✅ The products people actually view are near-real-time, and the cost scales with traffic, not catalog size.
- ❌ More moving parts: locking, rate limits, error states. The first visitor sees the cached price until the refresh lands. Needs Approach 1 underneath for list and search pages.

## Approach 3 — Partner feeds pushed to us ("price comparison network" model)
Ask brands (and later affiliate networks) to give us a product feed URL: Google-Merchant-format XML/CSV, or a Shopify collection feed. We ingest it on their schedule.
- Many D2C brands already keep a Google Merchant Center feed for Shopping ads, so asking for a read URL is a small favour.
- Offer something back: traffic, "verified by brand" badge, lab-report links.
- Indian affiliate networks may offer product feeds for marketplaces. Check terms and coverage before relying on this.
- Quick commerce (Blinkit, Zepto, Instamart): no public price API, and prices vary by pincode. Keep the current crowd availability reports. Don't scrape.

**Who does this:** price comparison sites such as PriceRunner and idealo, and Google Shopping's primary path, run on merchant-submitted feeds.

- ✅ Most accurate (brand-owned data, incl. SKUs and stock). No crawling. Scales to hundreds of brands.
- ❌ Depends on partnerships, so it's slow to start and coverage is uneven at first. Feeds can still go stale, so check `last_modified`.

---

## Recommendation
1. **This week, Approach 1 only:** run migration 016. Run `poll-d2c-prices` once by hand with `dry_run`, then for real. Check a few products. Uncomment its 6-hourly schedule. That alone replaces snapshots for most of the catalog.
2. **Next:** add the JSON-LD reader for non-Shopify brands. Turn Amazon search links into `/dp/<ASIN>` links and enable the Amazon schedule once Creators API access is approved.
3. **Then:** Approach 2 for product pages, once page-view numbers show which products matter.
4. **Ongoing:** Approach 3 outreach to the top 10 brands by clicks.

Guards to keep: the >50% jump check, at most 30% failed stores per run, history only on change, and a "checked X ago" label on every price.

## Sources
- Google Merchant Center: [automatic item updates](https://support.google.com/merchants/answer/12157888), [structured data for Merchant Center](https://support.google.com/merchants/answer/6069143)
- Skyscanner partner docs: [browse cache update frequency](https://skyscannerpartnersupport.zendesk.com/hc/en-us/articles/4686944252701-How-often-are-the-browse-cache-prices-updated), [cache vs live prices](https://skyscannerpartnersupport.zendesk.com/hc/en-us/articles/4686923517981-Why-does-the-Browse-Cache-API-not-match-that-of-the-live-pricing), [caching overview](https://skyscannerpartnersupport.zendesk.com/hc/en-us/articles/20917168737181)
- Amazon: [PA-API 5 deprecation → Creators API](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/paapiv5-deprecation)
