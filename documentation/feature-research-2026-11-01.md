# Feature Research (2026-11-01)

Companion to [codebase-audit-2026-11-01.md](codebase-audit-2026-11-01.md).

**Status:** see [feature-build-walkthrough.md](feature-build-walkthrough.md) for what was built and what wasn't.

**Reading the sources:** a link means an outside source. "Repo" means checked in the code. "Judgment" means opinion.

**How far this was checked:**
- Researched by a subagent, then reviewed in the main session.
- The Amazon policy and agreement wording below was re-read at the source, and the repo claims were re-checked.
- Other outside sources are as the research found them and were not re-verified.
- This is product research, not legal advice. Items marked **Legal check** need a lawyer.

**Corrections made during review:**
- The research said tagged Amazon links are "in the code". The tagging code exists, but it never runs for stored links, so 0 of 471 live links are tagged (audit C6).
- It said `price_history` already conflicts with Amazon's rules. The table has 0 rows, so nothing is in breach today. It would conflict once the poller runs.
- It cited section 11.3.3 for the 24-hour rule. The page read in review shows it as section 11 (PA API usage requirements), items 13-14.
- 12 variants are Tier 4; 8 of those carry the amino-spiking flag.

---

## Three findings that change the plan

### 1. Price-drop alerts and price charts are banned by Amazon unless it agrees

- Amazon India's [operating policy, clause 31](https://affiliate-program.amazon.in/help/operating/policies): "Unless otherwise agreed by Amazon, your site must not have price tracking and/or price alerting functionality."
- The [agreement](https://affiliate-program.amazon.in/help/operating/agreement), section 11 items 13-14: non-image content may be cached for up to 24 hours, then must be refreshed. A date/time stamp and disclaimer are required beside prices unless they refresh at least hourly.
- Repo: the poller writes every price to `price_history`, forever and publicly readable. This must change before Amazon polling starts.
- Clause 31 covers the whole site, so a chart of brand-store prices could also count (judgment).

### 2. The required notices are missing

- [Section 10](https://affiliate-program.amazon.in/help/operating/agreement) requires a clear and prominent "As an Amazon Associate I earn from qualifying purchases."
- Repo: that wording appears nowhere, and there is no privacy, terms or methodology page.

### 3. Live Amazon prices can't start yet

- Repo: no Amazon link is a real product page, and the poller skips search links.
- Amazon requires [10 qualifying sales in the past 30 days](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) for API access. Third-party guides say [access pauses if sales fall short](https://affiliatexblocks.com/docs/how-to-fix-amazon-api-associatenoteligible-error/).
- So traffic and tagged links must come before live-price features (judgment).

---

## What competitors do

| Who | What they offer | What we lack |
|---|---|---|
| [Trustified](https://www.trustified.in/) | Buys products anonymously and tests them blind. A [Pass/Fail list](https://www.trustified.in/passandfail) shows batch, date, lab, status and report link. Also a [Gold list](https://www.trustified.in/goldcertified), an app and YouTube memberships. [Brands can pay test charges](https://www.trustified.in/getcertified). | Any lab evidence |
| Unbox Health | [300+ products rated A+ to D](https://www.theweek.in/wire-updates/business/2025/11/14/dcm49-unbox-health.html), [split 50/50 between label accuracy and safety](https://unboxhealth.notion.site/Product-Rating-Methodology-fece27a8af6f4b56925493ab403708dc). [The public votes on what gets tested](https://m.thewire.in/article/ptiprnews/unbox-health-launches-the-great-indian-product-hunt-indias-first-public-vote-for-lab-testing-everyday-foods-and-supplements). | Test results, community votes |
| [TruthIn](https://the-ken.com/newsletters/two-by-two/what-happens-when-indian-consumers-know-what-they-are-eating/), [FactsScan](https://frontiertech.niti.gov.in/story/helping-indians-eat-healthier-the-app-that-demystified-food-labels-in-its-first-year/) | Apps that read and rate labels. TruthIn does no lab testing. | Label scanning |
| [HealthKart](https://www.healthkart.com/connect/10-best-whey-protein-powders-in-india-2026-muscleblaze-truebasics-more-ranked/) | Scored top-10 lists citing lab reports. MuscleBlaze and TrueBasics take the top three, and the article states no link to those brands. Uses price per kg, not per gram of protein. | Trusted buying guides (we can beat this on neutrality) |
| [Nutrabay](https://www.nutrabay.com/) | Says it sells direct with no third-party sellers. Has an authenticity page, wallet and app. | Authenticity check |
| MuscleBlaze | [SMS and QR checks](https://www.healthkart.com/sv/muscleblaze-bulk-gainer-with-creatine/SP-49873), [home test kit](https://www.nutraingredients.com/Article/2023/11/22/MuscleBlaze-gains-10-market-share-a-year-after-launching-whey-protein-test-kits/), [Amazon Transparency codes](https://brandservices.amazon.in/transparency/case-studies/muscleblaze) | Verification guidance |
| [Keepa](https://addons.mozilla.org/lt/android/addon/keepa), [Amazon Price History](https://www.businesstoday.in/technology/news/story/amazon-india-rolls-out-in-app-price-history-feature-502256-2025-11-14) | Price charts and alerts. Amazon's app shows 30 or 90 days. | Nothing we should copy |
| [Labdoor](https://Labdoor.com/about/testing) | Buys at retail, uses independent labs, grades five areas. [Criticised for unclear weighting](https://illuminatelabs.org/blogs/news/labdoor-review) (by a competitor). | Published scoring |
| [PriceSpy](https://pricespy.co.uk/information/about-pricespy) | Side-by-side compare, history, alerts, shop ratings | Compare view |
| [Cronometer](https://www.promealplan.com/en/blog/cronometer-vs-myfitnesspal) | Checked nutrition data, unlike crowd-entered MyFitnessPal (blog source) | Lesson: keep crowd data separate |

**Our opening (judgment):** test sites don't show ₹ per gram or store links, retailers aren't neutral, and price trackers ignore nutrition. No one found joins tests, ₹/g, many stores and local availability in one place.

---

## What Indian buyers worry about

- **Label honesty:** [25 of 36 products had less protein than claimed](https://www.nutraingredients.com/Article/2024/04/29/Protein-products-tested-in-India-don-t-meet-label-claims) ([study](https://pubmed.ncbi.nlm.nih.gov/38579036/)). A [critic argues](https://sudomakes.substack.com/p/5-problems-with-viral-supplement) the figure falls sharply with FSSAI's ±10% margin (blog, not peer reviewed). Unbox found [over 25% with label gaps](https://www.storyboard18.com/trending/over-half-of-popular-food-supplement-products-miss-top-ratings-in-lab-tests-87179.htm) in 30 products.
- **Fakes:** Delhi police [seized about 100 kg in March 2026](https://www.newsgram.com/delhi/2026/03/09/delhi-police-bust-fake-protein-supplement-racket), with fake Optimum Nutrition, Syntha-6 and Isopure labels and holograms. A [Noida case](https://www.stack3d.com/2024/12/counterfeit-supplements-caught-in-noida/) involved online sales. Buyers [call Amazon purchases "a bit risky"](https://www.desidime.com/discussions/finding-the-best-whey-protein-brand-in-india-2025?post_id=11632427).
- **Heavy metals:** lead was found in 27 of 36 products (same study). The critic says all but copper were within FSSAI limits. Unbox found about 10% above limits.
- **Price:** Keepa data for 11 whey products showed an [average 32% rise](https://www.thirdeyesight.in/2026/08/). Relief isn't expected before late 2026 or 2027.
- **Amino spiking** (cheap amino acids added to fake a higher protein reading): it needs [amino acid profiling to confirm](https://rippedbody.com/protein-powder-scams/), so a label can't prove it.
- **Taste, bloating, kidneys:** these come up [in forums](https://www.desidime.com/discussions/finding-the-best-whey-protein-brand-in-india-2025?post_id=11632427). That is anecdote only; no survey ranking them was found.
- **Lactose:** intolerance [rises from north to south](https://www.sciencealert.com/south-asias-dairy-intolerance-could-help-explain-our-ability-to-drink-milk). Exact percentages couldn't be verified.
- **Vegetarian status:** rennet (a cheese-making enzyme, animal or microbial) matters, and [makers often don't list its source](https://denzournutrition.com/blogs/whey-blogs/is-whey-protein-vegetarian) (seller blog).
- **Licensing:** a [Delhi raid in April 2026](https://www.newsgram.com/india/2026/04/25/illegal-performance-enhancing-drugs-expired-supplements-seized-in-delhi-raid) found supplements sold without a valid licence.
- **Who they trust:** in a [Pune study of 121 gym-goers](https://cardiometry.net/issues/no20-november-2021/usage-nutritional-supplements), 51.2% took advice from trainers and 9.9% from dietitians.

---

## Ranked feature ideas

Effort is an estimate: S = up to 2 days, M = up to 2 weeks, L = longer.

### 1. Disclosure and honest-wording pack (S, Now, Legal check)
- **What:** Add the Amazon statement plus privacy, terms and "how we rate" pages. Replace unsupported claims (audit C5), and review the "Diabetic-Friendly" (15 variants) and "Lab Certified" (1 variant) tags.
- **Why:** Amazon requires the notices, and India's rules require [disclosing commercial ties](https://www.mondaq.com/india/social-media/1312524/ccpa-guidelines-for-misleading-advertisements-and-endorsements-2022).
- **Builds on:** `Footer.tsx`, `ProductDetail.tsx`, `constants.ts`, `red_flag_dictionary.json`, `protein_tier.py`.
- **Risk:** Rewording is a judgment call. "Contains added amino acids (from label)" is safer than "Spiked".

### 2. Amazon-safe pricing (M, Now, Legal check)
- **What:** Stop saving Amazon rows to `price_history`, or delete them within 24 hours. Show an exact date and time plus "Product prices and availability are accurate as of the date/time indicated and are subject to change." Hide Amazon prices older than 24 hours. Add real ASINs (Amazon product IDs).
- **Why:** Protects the affiliate account. A 6-hourly poll triggers the stamp rule, and "checked 3 h ago" may not satisfy it.
- **Builds on:** `poller.py`, `RedirectButtons.tsx`, `poll-prices.yml`, `redirect_links`.
- **Risk:** The India text names PA API; the [Creators API docs](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction) point to the same agreements. Assume the rule applies, and ask Amazon. Keep Amazon images out of Supabase Storage.

### 3. Lab evidence panel (M, Now, Legal check)
- **What:** A `test_reports` table (source, lab, batch, date, result, tested protein, report link), a product panel, and a "has recent report" filter. Show ₹/g on tested protein beside label ₹/g.
- **Why:** Answers the buyers' biggest fear. [Trustified's format](https://www.trustified.in/passandfail) proves the fields work, and brands like [The Whole Truth](https://twtprotein.notion.site/Protein-Lab-Test-Reports-1d0fae391f3f4c8f9f398306890cedff) publish batch reports.
- **Builds on:** `ProductDetail.tsx`, `FilterPanel.tsx`, `useFilters.ts`, `metrics.ts`.
- **Risk:** Results apply to one batch, so always show batch and date. Link out rather than copying, ask Trustified and Unbox for permission, and label brand-supplied reports. Start with the top 50 powders.

### 4. Compare page with share link (S to M, Now)
- **What:** `/compare?v=a,b,c` from the shortlist, showing ₹/g, density, sugar, flags and test status, with a shareable link and preview image. Add a few hand-picked pairs.
- **Why:** Helps undecided buyers and the trainers who advise them. The cart text already promises "compare". [Google advises](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews) explaining what sets a product apart.
- **Builds on:** `CartContext`, `CartDrawer.tsx`, `metrics.ts`.

### 5. SEO base and value leaderboards (S then M, Now)
- **What:** `sitemap.ts`, `robots.ts`, `metadataBase` and [Product structured data](https://developers.google.com/search/docs/appearance/structured-data/product-snippet). Then a few server-rendered lists, such as lowest ₹/g whey isolate or bars without maltitol.
- **Why:** Results for these searches were mostly retailer, brand and affiliate blogs ([one small sample](https://www.healthkart.com/connect/10-best-whey-protein-powders-in-india-2026-muscleblaze-truebasics-more-ranked/)). Google favours [quantitative measurements and multiple sellers](https://developers.google.com/search/docs/specialty/ecommerce/write-high-quality-reviews).
- **Builds on:** `product/[slug]/page.tsx`, `data.ts`, `metrics.ts`.
- **Risk:** Mass pages can trigger [thin content penalties](https://developers.google.com/search/docs/essentials/spam-policies). Keep the list small and dated. Don't put stale Amazon prices in structured data.

### 6. "Is this genuine?" card (S then M, Now then Next, Legal check)
- **What:** Phase 1: the maker, FSSAI licence number, a link to [FoSCoS FBO Search](https://blog.petpooja.com/finance-compliance/fssai-licence-check-guide-ways-verify-food-business/) (FSSAI's licence lookup), and how to verify that brand's pack. Phase 2: show the Amazon seller and match it to our official list.
- **Why:** Commonly faked imports. Fakes are said to be [30-50% cheaper](https://www.nutraingredients.com/Article/2023/11/22/MuscleBlaze-gains-10-market-share-a-year-after-launching-whey-protein-test-kits/) (company claim).
- **Builds on:** `brands`, `ProductDetail.tsx`, `official_sellers.json` (6 brands, not used by the web or ETL source).
- **Risk:** The seller field couldn't be confirmed in Amazon's docs. Say "not on our list", never "fake".

### 7. Claim Check (S to M, Now, Legal check)
- **What:** Test product claims against FSSAI numbers already in the catalog. Secondary sources give ["high in protein"](https://compass.khaitanco.com/protein-on-trial-regulating-nutritional-claims-in-indias-growing-food-market) as at least 20% of RDA (recommended daily amount) per 100 g, and ["sugar-free"](https://www.taxclue.in/blog/regulation-5-schedule-i-fss-advertising-and-claims-regulations-2018-nutrition-claims/) as up to 0.5 g per 100 g.
- **Why:** Cheap, unique and uses existing data. 46 variants are tagged "High Protein".
- **Builds on:** `protein-etl/src/engine/`, `computePer100g`, `RedFlagBadges.tsx`.
- **Risk:** Confirm numbers against the gazette first. Word results as "our calculation", because a mistake could be defamatory.

### 8. Protein planner (S then M, Now then Next, Legal check)
- **What:** First a calculator for daily protein and ₹ per day or month. Then a short quiz on goal, diet, lactose and budget that returns a shortlist.
- **Why:** Helps beginners and price-squeezed buyers. No conversion data was found, so the uplift is unproven.
- **Builds on:** `user_preferences` (`body_weight_kg`, `daily_protein_target_g`, `max_budget_per_g`, unused today), `metrics.ts`, `useFilters.ts`.
- **Risk:** [ICMR-NIN's 2024 guidelines discourage protein supplements for muscle building](https://www.dtnext.in/lifestyle/wellbeing/why-do-icmr-nins-new-dietary-guidelines-advise-against-protein-supplements-784773). Mention food-first options, give no disease advice, and use a qualified reviewer (judgment).

### 9. Send shortlist to Amazon cart (S to M, Next)
- **What:** One button adds all shortlisted items to the Amazon cart.
- **Why:** Revenue. A click earns credit for [24 hours, and items added to cart in that window qualify if ordered within 89 days](https://affiliate-program.amazon.in/help/operating/agreement) (section 7).
- **Builds on:** `CartDrawer.tsx`, `redirect.ts`, ASINs from item 2.
- **Risk:** Confirm Amazon's current cart-link format.

### 10. Official partner links (M, Next)
- **What:** Add HealthKart, Nutrabay, Flipkart and brand programmes, through official affiliate programmes only.
- **Why:** More choice and income. Google suggests multiple sellers.
- **Builds on:** `redirect_links` platform CHECK, `PLATFORM_INFO`, `redirect.ts`.
- **Risk:** Terms are unclear: HealthKart is listed at [3%](https://earnkaro.com/blog/healthkart-affiliate-program/) or [2.7-4.73%](https://shopper.com/partnerships/healthkart-com-affiliate-program). Nutrabay's programme is unconfirmed. Commission must never affect rank.

### 11. Refill reminders and test-status watch (M, Next, Legal check)
- **What:** The retention loop to use instead of price alerts. Save products, then get a nudge when a tub should run out or a new test report appears. Start with email.
- **Builds on:** `user_favorites` (unused today), `user_activity`, `servings_per_pack`.
- **Risk:** WhatsApp marketing costs [about ₹0.86 per message, utility about ₹0.115](https://chatmaxima.com/whatsapp-api-pricing/india/), plus GST (vendor pages). iPhone web push [needs a home-screen install](https://documentation.onesignal.com/docs/web-push-for-ios). Link to our page, not Amazon. Needs clear opt-in.

### 12. Open scoring and Top Picks rebuild (M, Next, Legal check)
- **What:** Publish sub-scores for value, purity evidence and label flags, with the formula public.
- **Why:** Every "Best" award is simply the lowest ₹/g today, and "zero brand bias" sits beside a default sort that favours big brands (audit C5).
- **Builds on:** `topPicksConfig.ts`, `ranking.ts`, `metrics.ts`, item 3.
- **Risk:** [Ratings can create a "health halo"](https://the-ken.com/newsletters/two-by-two/what-happens-when-indian-consumers-know-what-they-are-eating/), so keep sub-scores visible.

### 13. Diet clarity fields (S to M, Next)
- **What:** Add brand-declared rennet source, lactose per serving and Jain status, each with a source.
- **Why:** 459 of 469 variants are tagged Vegetarian, but the schema has no rennet field. Only 2 are tagged Jain.
- **Builds on:** `product_variants`, `canonicalDietaryTag`, `FilterPanel.tsx`.
- **Risk:** Show "brand says", not a verified claim. Filling these fields is manual.

### 14. Taste and digestion ratings (M, Later, Legal check)
- **What:** Signed-in buyers rate taste, mixing and bloating, shown separately from lab data.
- **Builds on:** `user_activity`, the `availability_reports` pattern.
- **Risk:** Spam and paid reviews, so it needs moderation. Fix rate limiting first (audit H8).

### 15. Community test fund (L, Later, Legal check)
- **What:** Users vote on what to test, and the site funds tests at independent labs.
- **Why:** A real moat. [Unbox](https://m.thewire.in/article/ptiprnews/unbox-health-launches-the-great-indian-product-hunt-indias-first-public-vote-for-lab-testing-everyday-foods-and-supplements) and [Trustified](https://www.trustified.in/) both use voting.
- **Risk:** Lab cost is unknown, and legal exposure is highest here. Only do it after traffic exists.

---

## Quick wins

1. Item 1: disclosure and wording pack.
2. Item 2, first part: stop storing Amazon history; add the time stamp and disclaimer.
3. Item 5, first part: sitemap, robots and structured data.
4. Item 4: compare page.
5. Item 6, phase 1: genuine-product card for the top 20 brands.

**Note:** the critical audit fixes come before all of these.

---

## Don't build

- **Price-drop alerts or price charts:** against Amazon policy unless it agrees in writing. Amazon's app [already shows history](https://www.businesstoday.in/technology/news/story/amazon-india-rolls-out-in-app-price-history-feature-502256-2025-11-14).
- **Quick-commerce scraping:** the 2026-09-26 decision stands, and nothing here needs it.
- **FoSCoS scraping, or bulk-copying Trustified or Unbox data:** link out or ask permission.
- **Paid ranking or sponsored "verified" badges:** this contradicts the Top Picks claim. The `PROJECT.md` plan for sponsored verification needs rethinking. [ASCI requires disguised ads to be labelled](https://www.khaitanco.com/thought-leaderships/ASCI-guidelines-on-deceptive-design-patterns-in-digital-media-advertisements).
- **Cashback for using our Amazon links:** [purchases tied to incentives don't qualify](https://affiliate-program.amazon.in/help/operating/agreement).
- **Native app now:** sales through unapproved apps don't qualify, and `PROJECT.md` already defers it.
- **One overall "health score":** too easy to misread, and hard to defend.
- **Mass AI-written pages:** a [spam policy risk](https://developers.google.com/search/docs/essentials/spam-policies).
- **Barcode scanner:** the seed catalog has 0 barcodes, and scanner apps are crowded.
- **Diabetes or kidney advice filters:** too close to disease claims.

---

## Money and legal limits

**Money**
- [Amazon India rates, Oct-Nov 2026](https://affiliate-program.amazon.in/help/node/topic/GRXPHT8U84RAYDXZ): Health, Household & Personal Care 4%, Sports & Fitness 4.72%, Grocery 2.5%, all other 5%. Which category protein powder falls under isn't stated, so confirm it.
- At 4%, a ₹3,000 tub earns at most ₹120. Income needs volume and cart attribution.
- Labelled ads kept separate from rankings are fine. The rank itself must not be for sale.

**Legal (needs a lawyer)**
- **Lab criticism:** Delhi HC in [San Nutrition](https://www.livelaw.in/amp/high-court/delhi-high-court/san-nutrition-defamation-trademark-infringement-influencers-prima-facie-fair-comment-290617) refused to block lab-backed reviews, but that was [only an interim order](https://compass.khaitanco.com/protein-on-trial-regulating-nutritional-claims-in-indias-growing-food-market). In [Marico](https://spicyip.com/2020/01/brand-protection-in-the-age-of-social-media-influencers-bom-hc-in-parachute-disparagement-case.html), the Bombay HC ordered a takedown of a reckless review by someone promoting rival products. This site earns from rival products, so back every negative claim with evidence (judgment). The Marico appeal outcome wasn't found.
- **Penalties:** [up to ₹10 lakh for misleading food ads, up to ₹50 lakh from CCPA](https://compass.khaitanco.com/protein-on-trial-regulating-nutritional-claims-in-indias-growing-food-market) (the consumer protection authority). Nothing was found on how these apply to comparison sites.
- **DPDP (India's data protection law):** rules were [notified in November 2025](https://www.barandbench.com/amp/story/view-point/meity-notifies-final-digital-personal-data-protection-rules-2025), with main duties due around [May 2027](https://ogma.in/blog/dpdpa-technical-implementation-playbook-13-month-roadmap-to-may-2027). Expect [plain-language notice, no pre-ticked boxes and breach reports](https://www.seclore.com/fundamentals/dpdp-rules-2025-compliance-guide/). Under-18s need parental consent. No small-business exemption was found. `user_activity` and `user_searches` still need the "clear my history" control flagged in [suggested-for-you-walkthrough.md](suggested-for-you-walkthrough.md).

---

## Sources that couldn't be reached

- **Reddit:** blocked. One search snippet plus DesiDime, TechEnclave and Team-BHP were used instead. All anecdotal.
- **Unbox:** `unboxhealth.in` failed and the methodology page loaded empty, so the formula comes from a search snippet.
- **FSSAI and FoSCoS:** the claims compendium PDF returned 404, so thresholds are secondary. FoSCoS steps come from commercial guides.
- **Google:** its rule on `rel="sponsored"` couldn't be confirmed from its own docs.
- **Nothing reliable found:** Examine, MyProtein tools, BuyHatke and Pricebefore details, or Nutrabay's affiliate terms.
- **No data found:** alert, quiz or calculator uplift in India, or any survey ranking taste against price.
- **Amazon email rules:** the India policy shows no email clause. A [tracker of the US policy](https://conductatlas.com/platform/amazon-associates/amazon-associates-program-policies/) lists opt-in rules for email and SMS. Assume they apply until Amazon says otherwise.
