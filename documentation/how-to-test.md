# How to Test

Hands-on checklist for everything added in Phase 3 (metric filters, pincode / availability, live Amazon prices,
price poller) and the product discovery pipeline (Shopify + OCR + Gemini). Work top to bottom: each part only
needs the parts above it.

Commands assume Windows + Git Bash or PowerShell from the repo root `protien-searchtool/`.

---

## 0. One-time setup

```bash
# Python ETL (3.11+)
cd protein-etl
pip install -e ".[dev,ocr]"      # dev = pytest, ocr = RapidOCR + onnxruntime
cp .env.example .env             # fill in later sections as you get keys

# Website
cd ../protein-web
npm install
cp .env.local.example .env.local
```

## 1. Quick checks (no keys needed)

```bash
# Website: types, lint, and Vitest unit tests
cd protein-web
npx tsc --noEmit
npm test
npx eslint src/lib src/hooks src/components/search src/components/product/RedirectButtons.tsx src/components/location src/app/api

# ETL: unit tests (metrics, text match, red flags, protein tier, models, parsers, links, pricing, uploader, cli, discovery)
cd ../protein-etl
python -m pytest -q
```
Expected: no type errors, 66 frontend Vitest tests pass, 180 ETL pytest tests pass.
(`npx eslint src` on everything reports ~115 older problems in files Phase 3 didn't touch — a separate cleanup.)

## 2. Website without a database (seed data)

```bash
cd protein-web
npm run dev          # open http://localhost:3000
```
Leave the Supabase values in `.env.local` as placeholders: the site uses the 100 built-in seed products.

**Metric filters** — go to `/explore`:
- [ ] Filter panel shows **Protein Metrics** with 4 sliders; each shows "Any" at its far end.
- [ ] Move "Max ₹ per g protein" down → product count drops; URL gains `max_cost=…`.
- [ ] "Max calories per g protein" near 4–6 leaves only lean products (isolates).
- [ ] Sort dropdown has "Protein per ₹100 — High to Low" and "Calories per g Protein — Low to High"; order changes.
- [ ] Reload the page with the URL params → same filters are restored. **Reset** clears them.
- [ ] Mobile width: the ⚙️ Filters badge counts the active sliders.
- [ ] Repeat on a category page, e.g. `/category/protein-powders`.

**Mobile Navigation & Layout** — open in mobile view or shrink browser width:
- [ ] Navbar row 2 shows "Home", "Top Picks", and a "Categories" dropdown.
- [ ] Clicking "Categories" expands a searchable dropdown list of categories.
- [ ] Unscrolled state: Navbar shows logo, website name, search bar icon, login, and cart. Clicking search icon hides website name, expands search bar, and collapses login/cart to icons only.
- [ ] Scroll down: Website name disappears, search bar icon expands to search input, and login/cart buttons show icons only.
- [ ] Cart button is cleanly visible on mobile without overflowing text ("Independent Platform" text removed).
- [ ] Touch/tap check: Verify there are no hover effects triggered on mobile for product cards or buttons.

**Pincode** — on the filter panel or any product page:
- [ ] Save button is disabled until 6 digits (not starting with 0) are entered.
- [ ] After saving, "Delivering to 560034 · Change" shows in both the filter panel and product page (same browser).
- [ ] "Only products reported … near me" checkbox is disabled without a pincode.

**Product page** — open any product:
- [ ] Core metrics show MRP, Calories, and Protein (Calories replaces Protein Density).
- [ ] MRP, Calories, and Protein labels are center-aligned and share the orange accent color (`#F59E0B`) matching the brand name.
- [ ] Brand name is prominently sized and bright white MRP is clearly readable.
- [ ] Amazon card shows a price (seed price, no "checked" time without a database).
- [ ] Blinkit / Zepto / Instamart show "Availability depends on your area" or "No reports near <pincode> yet".
- [ ] Independent platform links have the smooth ambient glow and amber border hover effect on desktop.
- [ ] Links open the platform search in a new tab.

## 3. Database (Supabase)

1. Create a project at supabase.com.
2. SQL editor → run `supabase/migrations/001_schema.sql` … `005_prices_availability.sql` **in order**.
3. Keys:
   - `protein-web/.env.local`: `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`.
   - `protein-etl/.env`: `SUPABASE_URL`, `SUPABASE_SERVICE_KEY` (service role — never put it in the website).
4. Upload the seed catalogue:
   ```bash
   cd protein-etl
   python scripts/seed.py --dry-run   # check first
   python scripts/seed.py
   ```
5. Restart `npm run dev`.

Checks:
- [ ] Explore shows the database products; **all** filters and sorts work (this was broken before Phase 3).
- [ ] Product page Amazon card shows "₹X · checked N ago".
- [ ] Click a Blinkit link → "Was it available on Blinkit near <pincode>?" → **Yes** → "Thanks…" message.
- [ ] Supabase table editor → `availability_reports` has the row; `availability_summary` shows yes_count 1.
- [ ] Product page now says "Reported in stock near you (1 yes / 0 no)".
- [ ] Explore → tick "near me" → only that product remains.
- [ ] A pincode from a different district (first 3 digits differ) shows "No reports … yet".

## 4. Page refresh endpoint

Set `REVALIDATE_SECRET=<long random string>` in `protein-web/.env.local`, restart, then:
```bash
curl -i -X POST http://localhost:3000/api/revalidate -H "Authorization: Bearer <secret>"   # 200 {"revalidated":true}
curl -i -X POST http://localhost:3000/api/revalidate -H "Authorization: Bearer wrong"      # 401
```

## 5. Amazon price poller

Needs Supabase (section 3) **and** Amazon Creators API access (Associates account with 10 qualifying sales in 30 days).
Also replace the placeholder Amazon links in `protein-etl/data/seed_products.json` with real `https://www.amazon.in/dp/<ASIN>` URLs and re-seed.

```bash
cd protein-etl
python src/cli.py --dry-run poll-prices    # reads + reports, writes nothing
python src/cli.py poll-prices              # writes
```
- [ ] Without Amazon keys: clear "credentials missing" message, exit code 1.
- [ ] Dry run lists checked / updated / skipped (search links are skipped: "no ASIN").
- [ ] Live run: `redirect_links.platform_price_inr` + `price_last_checked` change, `price_history` gains rows,
      `product_variants.best_price_inr` / `best_cost_per_g_protein` update.
- [ ] A >50% price jump is skipped unless `--force`.
- [ ] With `REVALIDATE_URL` + `REVALIDATE_SECRET` in `.env`: "Website pages refreshed."
- [ ] If Amazon's token/API URLs differ from the defaults, set `AMAZON_CREATORS_TOKEN_URL` / `AMAZON_CREATORS_API_URL`.

**Scheduled run (GitHub Actions)** — repo Settings → Secrets and variables → Actions → add every variable used in
`.github/workflows/poll-prices.yml`. Then Actions tab → "Poll Amazon prices" → **Run workflow** once by hand.

## 6. Product discovery (Shopify → drafts)

No keys needed for the free layers + OCR. The first OCR run downloads its models (one time, ~tens of MB).

```bash
cd protein-etl
python src/cli.py discover --brand Nakpro --limit 3 --readers ocr     # free
python src/cli.py discover --limit 3                                   # OCR, then Gemini if GEMINI_API_KEY is set
```
- [ ] Table per brand with `ready` / `needs_input` rows; muesli, combos and non-protein items are skipped.
- [ ] Files appear in `protein-etl/data/drafts/`; each has `nutrition_source`, `layers_tried`, `warnings`.
- [ ] Running again skips products already drafted ("exists"); `--refresh` redrafts them.
- [ ] Without the OCR install: "OCR skipped: install it…" and discovery still runs.

## 7. OCR vs Gemini comparison

Add `GEMINI_API_KEY` to `protein-etl/.env` (Google AI Studio). Cost: ~$0.02 per product, cached after the first read.

```bash
cd protein-etl
python src/cli.py compare-readers --limit 3                  # all brands in data/brands.json
python src/cli.py compare-readers --brand SuperYou --limit 5
```
- [ ] Console table: complete / partial / nothing / errors / average seconds / estimated $ per reader, plus agreement %.
- [ ] Report saved to `documentation/reader-comparisons/<date-time>.md` (+ `.json`).
- [ ] Open each product page link, find the nutrition label photo, and fill **Correct on pack?** (✅/❌ per reader).
- [ ] Decide the default order for `--readers` from the scores (e.g. keep `ocr,gemini` if OCR is usually right,
      switch to `gemini` if OCR is mostly wrong or partial).
- [ ] Running the same comparison again costs $0 for Gemini (cached) — the report shows "(cached)".

## 8. Review and publish drafts

```bash
cd protein-etl
python src/cli.py --dry-run review    # practise: nothing uploaded, files still move to approved/rejected
python src/cli.py review              # live (needs Supabase keys)
```
- [ ] Each draft shows source, layers tried, warnings, then the normal preview (₹/g, calories, red flags, protein tier).
- [ ] `needs_input` drafts list the exact missing fields — fix them in the JSON file, then run `review` again.
- [ ] Approve → product appears on `/explore` immediately; other pages after the refresh call (or within 1–24 h).
- [ ] Reject → file moves to `data/drafts/rejected/` and `discover` never suggests it again.

---

## Known gaps while testing
- `protein-web/middleware.ts` is outside `src/`, so login session refresh doesn't run (separate fix).
- Availability reports have no rate limiting yet — don't open the site publicly until that's added.
- Only SuperYou, Nakpro and Yoga Bar are in `data/brands.json`; add more Shopify brands there.
