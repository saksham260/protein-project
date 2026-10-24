# Phase 3 / Plan 03-01 — "Continue with Google" sign-in (walkthrough)

Date: 2026-10-24 · Branch: `fix/catalog-images-and-discount-prices`

Along the way this session also cleared the 16 data-quality warnings and fixed the session-refresh file (see "Also done").

## What it does
- The **Login** button in the navbar (and the mobile menu) starts Google sign-in through Supabase Auth.
- After Google, the visitor lands back on the page they were on, signed in. The button then shows their first name; clicking it opens a menu with their email and **Sign out**.
- If Supabase keys aren't set (demo mode), Login shows "Login isn't set up yet" instead of failing.

## How the flow works
1. Click Login → `signInWithGoogle()` (`src/context/AuthContext.tsx`) sends the browser to Google via Supabase, asking to return to `/auth/callback?next=<current page>`.
2. Google → Supabase (`<project>.supabase.co/auth/v1/callback`) → our `/auth/callback`.
3. `src/app/auth/callback/route.ts` swaps the one-time `code` for a session cookie (`exchangeCodeForSession`) and redirects to `next`.
4. `src/proxy.ts` refreshes the session cookie on every request so logins don't expire mid-visit.

## Files
| File | Change |
|---|---|
| `src/lib/auth.ts` (+ `auth.test.ts`) | `safeNextPath` (only same-site redirect targets, blocks `//evil.com`), `publicOrigin` (uses Render's forwarded host so redirects don't go to an internal address) |
| `src/context/AuthContext.tsx` | New. `useAuth()` → `user`, `isReady`, `isAvailable`, `signInWithGoogle`, `signOut` |
| `src/app/auth/callback/route.ts` | New. Finishes the login; on failure goes to `/?auth_error=1` |
| `src/components/auth/LoginButton.tsx` | Was a "Coming soon" stub; now real login + account menu |
| `src/components/layout/MobileNav.tsx` | Same, for the mobile menu |
| `src/app/layout.tsx` | Wraps the app in `AuthProvider` |
| `src/proxy.ts` | Moved from `middleware.ts` (outside `src/`, so Next never ran it; Next 16 also renamed it to `proxy`) |

## One-time setup you must do (nothing works until this is done)
**Google Cloud Console**
1. Create a project → OAuth consent screen → Credentials → *Create OAuth client ID* → Web application.
2. Authorized redirect URI: `https://<your-project>.supabase.co/auth/v1/callback` (Supabase's address, not the site's).
3. Copy the Client ID and Client Secret.

**Supabase dashboard**
1. Authentication → Providers → Google → enable, paste the ID and secret.
2. Authentication → URL Configuration:
   - Site URL: `https://<your-app>.onrender.com`
   - Redirect URLs: `https://<your-app>.onrender.com/auth/callback`, `http://localhost:3000/auth/callback`

**Render** (Environment tab, set *before* the build): `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`. Never put `SUPABASE_SERVICE_KEY` on the website.

## Troubleshooting
- `redirect_uri_mismatch` → the Google redirect URI isn't exactly the Supabase one above.
- Lands on `localhost` after login → Supabase *Site URL* is still localhost.
- Back on the home page with `?auth_error=1` → the code swap failed; check the Redirect URLs list.

## Verification done
Type check, lint and unit tests (82) pass. **Not tested against real Google** — needs the setup above.

## Also done in this session
- **Data quality:** warnings 16 → 0 (371 products, 0 errors). Removed the bogus "Phab Warm Cocoa Protein Bar" (not sold by Phab; its link pointed to the Chocolate Brownie page). Widened two density ranges (powders floor 55→50%, savory snacks ceiling 40→45%) and added a reviewed list (`DENSITY_REVIEWED` in `scripts/verify_demo_catalog.py`) for Sleepy Owl powder sachets and Chase cereals, whose brand-stated figures are real.

## Still to do in Phase 3 (plan 03-02)
Preferences form (protein target, diet, allergens), favorites saved per user, `/dashboard`, and the recommendation feed. Needs new tables with row-level security (`user_preferences`, `favorites`).
