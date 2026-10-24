# "Suggested for You" — per-user activity (walkthrough)

Date: 2026-10-24

## What it does
- The home page "Suggested for You" section is shown **only when signed in**. Logged-out visitors don't see it.
- It lists the products the person **last viewed** or **clicked through to a purchase page** for, newest first (max 8, one card per product). Products they clicked through to buy carry a "Went to buy" tag.
- Brand-new users (no history yet) see a short "Nothing here yet" message with a link to browse.

## Database
`supabase/migrations/011_user_activity.sql` (also appended to `setup_all.sql`, and listed in `verify.sql`):

| Column | Meaning |
|---|---|
| `user_id` | who (links to `users`, deleted with the user) |
| `product_id` / `variant_id` | what they looked at |
| `event_type` | `view` or `purchase_click` |
| `platform` | for clicks: amazon / blinkit / zepto / instamart / d2c |
| `created_at` | when |

Row-level security: each person can read, add and delete **only their own rows**. Includes the Data API grant (`SELECT, INSERT, DELETE` for signed-in users) required by this Supabase project.

**Must be applied by hand:** Supabase dashboard -> SQL Editor -> paste `011_user_activity.sql` -> Run. Until then, saving activity fails quietly and the section shows "Nothing here yet".

## Web code
| File | Role |
|---|---|
| `src/lib/activity.ts` | `logActivity`, `getRecentActivity`, and `recentProducts` (turns rows into one-per-product, newest first, flagged if they went to buy). Tests in `activity.test.ts` |
| `src/components/product/ProductViewTracker.tsx` | Renders nothing; saves a `view` when a signed-in user opens a product (once per browser session per product) |
| `src/components/product/RedirectButtons.tsx` | Saves a `purchase_click` when a signed-in user clicks any purchase button (new `productId` prop) |
| `src/components/product/SuggestedForYou.tsx` | The home-page section (hidden when logged out) |
| `src/app/HomeClient.tsx` | Old generic "mix of 8 products" removed; uses `SuggestedForYou` |
| `src/components/product/ProductDetail.tsx` | Adds the tracker and passes `productId` to the buttons |

## Notes and limits
- Nothing is saved for logged-out visitors.
- Works only with the live database: product ids must be real database ids.
- No "clear my history" button yet (the database already allows deleting own rows). Worth adding, and mention in a privacy policy, before launch.
- Not tested against the live database (migration not applied yet); checked with type check, lint and unit tests.
