# Recent searches in the search bar (walkthrough)

Date: 2026-10-24

## What it does
- When **signed in**, clicking the empty search bar in the navbar opens a **Recent searches** list (latest 8, newest first).
- Click an entry to search it again. Each row has an **x** to remove it, and **Clear all** empties the list.
- Searches are saved when the person presses Enter, submits the form, clicks "View all results", or clicks a suggested product while a search is typed.
- Searching the same thing again (any upper/lower case or spacing) moves it to the top instead of adding a duplicate.
- Logged-out visitors see nothing new, and nothing is saved for them. As soon as they start typing, the normal product suggestions appear as before.

## Database
`supabase/migrations/012_user_searches.sql` (also appended to `setup_all.sql`, listed in `verify.sql`):

| Column | Meaning |
|---|---|
| `user_id` | who |
| `query` | what they searched, as typed (2-80 characters) |
| `query_key` | lower-case, single-spaced form; one row per person per key |
| `created_at` | last time they searched it |

Row-level security: each person can read, add, refresh, and delete **only their own rows**. Includes the Data API grant for signed-in users.

**Must be applied by hand:** Supabase dashboard -> SQL Editor -> paste `012_user_searches.sql` -> Run. (Migration 011 for "Suggested for You" is also still to be run if it has not been.) Until then, nothing is saved and the list never appears.

## Code
| File | Role |
|---|---|
| `src/lib/searchHistory.ts` (+ test) | Tidy the typed text, keep the list de-duplicated, and save / read / delete rows |
| `src/hooks/useRecentSearches.ts` | The signed-in user's list, with instant updates and no-ops when signed out |
| `src/components/search/NavbarSearch.tsx` | Shows the list on focus, and saves searches |

## Limits
- Only the navbar search bar has the list for now. The large search box on the `/search` page does not.
- Stores search words, not the products opened from them. Product views are already kept for "Suggested for You".
- A privacy page should say that search history is stored for signed-in users and can be cleared.
